"""
Functions to find tiles coordinates for map_tiles_downloader.py

- tile: (zoom, x, y)
- tile_list: list of tiles [(zoom, x, y), ...]
- tile_dict: dict with zoom levels as keys and tile_list as value {0: [(zoom, x, y), ...], ...}
- minmax_tiles: tile_dict with topleft and bottom right tiles for each zoom level
    {0: [(zoom_tl, x_tl, y_tl), (zoom_br, x_br, y_br)], ...}
"""

from time import sleep
from random import randint
from shutil import copyfileobj
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import os
import math
import requests


def estimate_tile_list_size(tile_list):
    """
    Estimate the disk size of the tiles.
    """
    tile_size = 20  # In KB
    print("Nombre de tuiles:", len(tile_list))
    if len(tile_list) * tile_size < 10_000:
        print("Taille KB :", len(tile_list) * tile_size)
    else:
        print("Taille MB :", round(len(tile_list) * tile_size / 1000))


def tiles_between(topleft, botright):
    """
    Get the tile list between two tiles. Zoom level must be the same.

    Args:
        topleft: Tile (zoom, x, y)
        botright: Tile (zoom, x, y)

    Returns:
        List of tiles (zoom, x, y)
    """
    tile_list = []
    z = topleft[0]
    for x in range(topleft[1], botright[1] + 1):
        for y in range(topleft[2], botright[2] + 1):
            tile_list.append((z, x, y))

    return tile_list


def download_tiles(tile_list, folder="./tiles/"):
    """
    Download all tiles of the list in a folder using the z/x/y.png structure.

    Args:
        tile_list: List of tiles (zoom, x, y) to download
        folder: Folder to save the tiles
    """
    for tile in tile_list:
        # Timeout to not overload the server
        sleep((100 + randint(-50, 200)) / 1000)

        zxy_path = f"{tile[0]}/{tile[1]}/{tile[2]}.png"
        base_url = "https://tile.geofabrik.de/549e80f319af070f8ea8d0f149a149c2/"
        url = urljoin(base_url, zxy_path)

        filepath = os.path.join(folder, zxy_path)
        if os.path.exists(filepath):
            print("Tile already exists:", filepath)
            continue

        headers = {
            "Accept": "*/*",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "tile.geofabrik.de",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36",
        }

        print("Downloading:", url)
        res = requests.get(url, stream=True, headers=headers, timeout=100)

        if res.status_code == 200:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                copyfileobj(res.raw, f)
            print("Image successfully downloaded:", filepath)
        else:
            print("Image couldn't be retrieved", res.status_code)


def download_tile_dict(tile_dict, folder="./tiles/"):
    """
    Download all tiles from a dictionary.

    Args:
        tile_dict: Dict with zoom levels as keys and list of tiles as values.
        folder: Folder to save the tiles.
    """
    for tile_list in tile_dict.values():
        download_tiles(tile_list, folder)


def tile_from_lat_lon(zoom, lat_deg, lon_deg):
    """
    Calculates the Z/X/Y tile coordinates for a given latitude, longitude, and zoom level.

    Args:
        zoom: Zoom level.
        lat_deg: Latitude in degrees.
        lon_deg: Longitude in degrees.

    Returns:
        A tuple containing the (zoom, x, y) tile coordinates.
    """
    lat_rad = math.radians(lat_deg)
    n = pow(2, zoom)
    x = int((lon_deg + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return (zoom, x, y)


def coords_string_from_kml_file(kml_file_path):
    """
    Extracts coordinates from a KML file.

    Args:
        kml_file_path: Path to the KML file relative to the kml_files directory.

    Returns:
        A string of coordinates in the format "lon,lat,alt lon,lat,alt ...".
    """
    file_dir = os.path.dirname(os.path.realpath(__file__))
    kml_file_path = os.path.join(file_dir, kml_file_path)

    if not os.path.exists(kml_file_path):
        raise FileNotFoundError(f"KML file not found: {kml_file_path}")
    tree = ET.parse(kml_file_path)
    root = tree.getroot()
    coords = root.findall(".//{http://www.opengis.net/kml/2.2}coordinates")
    return str(coords[0].text).strip()


def minmax_tiles_from_coords_string(coords_string, zoom_start, zoom_stop):
    """
    Get the minmax tiles from the coordinates string.

    Args:
        coords_string: The coordinates string in the format "lon,lat,alt lon,lat,alt ..."
        zoom_start: The starting zoom level.
        zoom_stop: The stopping zoom level.

    Returns:
        A dictionary with zoom levels as keys and list of top left and bottom right tiles as values
        {0: [(zoom_tl, x_tl, y_tl), (zoom_br, x_br, y_br)], ...}
    """
    lat_list = []
    lon_list = []
    for coord in coords_string.split(" "):
        lon, lat, _ = map(float, coord.split(","))
        lat_list.append(lat)
        lon_list.append(lon)

    tile_dict = {}
    for zoom in range(zoom_start, zoom_stop + 1):
        # Convert lat/lon to tile coordinates
        topleft = tile_from_lat_lon(zoom, max(lat_list), min(lon_list))
        botright = tile_from_lat_lon(zoom, min(lat_list), max(lon_list))
        tile_dict[zoom] = ((zoom, topleft[1], topleft[2]), (zoom, botright[1], botright[2]))

    return tile_dict


def minmax_tiles_from_radius(lat, lon, radius, zoom_start, zoom_stop):
    """
    Calculates the minimum and maximum tile coordinates for a given latitude, longitude, and radius.

    Args:
        lat: Latitude in degrees.
        lon: Longitude in degrees.
        radius: Radius in kilometers.
        zoom_start: The starting zoom level.
        zoom_stop: The stopping zoom level.

    Returns:
        A dictionary with zoom levels as keys and list of top left and bottom right tiles as values
        {0: [(zoom_tl, x_tl, y_tl), (zoom_br, x_br, y_br)], ...}
    """
    tile_dict = {}
    for zoom in range(zoom_start, zoom_stop + 1):
        # Approximate conversion from kilometers to degrees latitude
        lat_offset = radius / 111.32
        # Approximate conversion from kilometers to degrees longitude
        lon_offset = radius / (111.32 * math.cos(math.radians(lat)))

        # Get the top left and bottom right tile coordinates
        topleft = tile_from_lat_lon(zoom, lat + lat_offset, lon - lon_offset)
        botright = tile_from_lat_lon(zoom, lat - lat_offset, lon + lon_offset)

        tile_dict[zoom] = ((zoom, topleft[1], topleft[2]), (zoom, botright[1], botright[2]))

    return tile_dict


def print_minmax_tiles(tile_dict):
    """
    Prints the minimum and maximum tile coordinates for each zoom level.

    Args:
        tile_dict: A list of tuples containing the ((min_x, min_y), (max_x, max_y))
        coordinates of the tiles.
    """
    print("Tile list:")
    for zoom, (topleft, botright) in sorted(tile_dict.items()):
        print(f"Zoom: {zoom}")
        print(f"  Top left  : ({topleft[1]}, {topleft[2]})")
        print(f"  Bot right : ({botright[1]}, {botright[2]})")


if __name__ == "__main__":
    # Print calculated tile list to help building functions in map_tiles_downloader.py

    #################### Launch Canada Launchsite ####################
    launch_canada_launchsite_coords = (47.977647, -81.857583)
    print("Launch Canada Launchsite 15km radius tiles:")
    print_minmax_tiles(
        minmax_tiles_from_radius(
            launch_canada_launchsite_coords[0],
            launch_canada_launchsite_coords[1],
            15, 8, 13
        )
    )
    print("Launch Canada Launchsite 10km radius tiles:")
    print_minmax_tiles(
        minmax_tiles_from_radius(
            launch_canada_launchsite_coords[0],
            launch_canada_launchsite_coords[1],
            10, 12, 15
        )
    )
    print("Launch Canada Launchsite 5km radius tiles:")
    print_minmax_tiles(
        minmax_tiles_from_radius(
            launch_canada_launchsite_coords[0],
            launch_canada_launchsite_coords[1],
            5, 12, 15
        )
    )

    #################### Launch Canada Timmins ####################
    print("Launch Canada Timmins tiles:")
    print_minmax_tiles(
        minmax_tiles_from_coords_string(
            coords_string_from_kml_file("kml_files/Timmins.kml"),
            5, 15
        )
    )

    #################### IREC 2025 Launchsite ####################
    irec_launchsite_coords = (31.043707, -103.528598)
    print("IREC 2025 Launchsite 20 km radius tiles:")
    print_minmax_tiles(
        minmax_tiles_from_radius(
            irec_launchsite_coords[0],
            irec_launchsite_coords[1],
            20, 8, 14
        )
    )
    print("IREC 2025 Launchsite 15 km radius tiles:")
    print_minmax_tiles(
        minmax_tiles_from_radius(
            irec_launchsite_coords[0],
            irec_launchsite_coords[1],
            15, 12, 16
        )
    )
    print("IREC 2025 Launchsite 10 km radius tiles:")
    print_minmax_tiles(
        minmax_tiles_from_radius(
            irec_launchsite_coords[0],
            irec_launchsite_coords[1],
            10, 12, 16
        )
    )

    #################### IREC Midland ####################
    print("IREC Midland tiles (large):")
    print_minmax_tiles(
        minmax_tiles_from_coords_string(
            coords_string_from_kml_file("kml_files/Midland - Large.kml"),
            5, 14
        )
    )
    print("IREC Midland tiles (small):")
    print_minmax_tiles(
        minmax_tiles_from_coords_string(
            coords_string_from_kml_file("kml_files/Midland - Small.kml"),
            12, 16
        )
    )
