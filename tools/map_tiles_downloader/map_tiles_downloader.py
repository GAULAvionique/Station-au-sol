"""
Script to download OSM map tiles from Geofabrik.

Tile number needs to be limited to avoid overloading the server.

To find the tile numbers, you can use the Geofabrik map tool:
https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1#3/53.0188/-82.7651
"""

# Spaceport (New Mexico):
# (32.98950, -106.97509)

# IREC (Texas):
# (31.043707, -103.528598)

# Launch Canada (Launch Site):
# (47.977647, -81.857583)

# Launch Canada (Timmins):
# (48.475804, -81.338665)

from map_tiles_calculator import tiles_between, download_tiles


def get_north_america_base_tiles():
    """
        List of base tiles for North America.
        Zoom level 0 to 5.
    """
    return [
        (0, 0, 0),
        *tiles_between((1, 0, 0), (1, 1, 1)),  # 4 tiles, ~80KB
        *tiles_between((2, 0, 0), (2, 1, 1)),  # 4 tiles, ~80KB
        *tiles_between((3, 1, 2), (3, 2, 3)),  # 4 tiles, ~80KB
        *tiles_between((4, 2, 5), (4, 4, 6)),  # 6 tiles, ~120KB
        *tiles_between((5, 4, 10), (5, 10, 13)),  # 28 tiles, ~560KB
        # Total: 46 tiles, ~0.92MB
    ]


def get_ulaval_tiles():
    """
        List of tiles for Université Laval.
        Zoom level 6 to 15.
    """
    return [
        *tiles_between((6, 18, 22), (6, 19, 23)),  # 4 tiles, ~80KB
        *tiles_between((7, 37, 44), (7, 39, 45)),  # 6 tiles, ~120KB
        *tiles_between((8, 76, 89), (8, 77, 90)),  # 4 tiles, ~80KB
        *tiles_between((9, 153, 179), (9, 155, 181)),  # 9 tiles, ~180KB
        *tiles_between((10, 308, 360), (10, 309, 361)),  # 4 tiles, ~80KB
        *tiles_between((11, 617, 721), (11, 619, 722)),  # 6 tiles, ~120KB
        *tiles_between((12, 1236, 1443), (12, 1237, 1444)),  # 4 tiles, ~80KB
        *tiles_between((13, 2472, 2887), (13, 2475, 2889)),  # 12 tiles, ~240KB
        *tiles_between((14, 4947, 5776), (14, 4948, 5777)),  # 4 tiles, ~80KB
        *tiles_between((15, 9895, 11553), (15, 9897, 11555)),  # 9 tiles, ~180KB
        # Total: 62 tiles, ~1.24MB
    ]


def get_spaceport_launchsite_tiles():
    """
        List of tiles for Spaceport America launchsite (New Mexico).
        (32.98950, -106.97509)
        Zoom level 6 to 15.

        https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1&mlat=32.9895&mlon=-106.97509#12/32.9895/-106.9751
    """
    return [
        *tiles_between((6, 12, 25), (6, 13, 26)),  # 4 tiles, ~80KB
        *tiles_between((7, 25, 50), (7, 26, 51)),  # 4 tiles, ~80KB
        *tiles_between((8, 51, 102), (8, 52, 103)),  # 4 tiles, ~80KB
        *tiles_between((9, 103, 205), (9, 104, 206)),  # 6 tiles, ~120KB
        *tiles_between((10, 206, 411), (10, 208, 413)),  # 9 tiles, ~180KB
        *tiles_between((11, 413, 823), (11, 417, 826)),  # 20 tiles, ~400KB
        *tiles_between((12, 827, 1647), (12, 834, 1652)),  # 48 tiles, ~960KB
        *tiles_between((13, 1655, 3295), (13, 1668, 3304)),  # 140 tiles, ~2800KB
        *tiles_between((14, 3311, 6591), (14, 3336, 6608)),  # 468 tiles, ~9360KB
        # *tiles_between((15, 6623, 13183), (15, 6672, 13216)),  # 1700 tiles, ~34000KB
        # Total: 2403 tiles, ~48.06MB
        # Total without last zoom: 703 tiles, ~14.06MB
    ]


def get_irec_base_tiles():
    """
        List of base tiles for IREC (Texas).
        (31.043707, -103.528598)
        Zoom level 6 to 9.

        https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1&mlat=31.043707&mlon=-103.528598#7/31.0437/-103.5286
    """
    return [
        *tiles_between((6, 12, 25), (6, 14, 26)),  # 6 tiles, ~120KB
        *tiles_between((7, 25, 51), (7, 28, 53)),  # 12 tiles, ~240KB
        *tiles_between((8, 53, 103), (8, 55, 105)),  # 9 tiles, ~180KB
        *tiles_between((9, 107, 207), (9, 111, 210)),  # 20 tiles, ~400KB
        # Total: 47 tiles, ~0.94MB
    ]


def get_irec_launchsite_tiles():
    """
        List of tiles for IREC launchsite (Texas).
        (31.043707, -103.528598)
        Zoom level 10 to 15.

        https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1&mlat=31.043707&mlon=-103.528598#12/31.0437/-103.5286
    """
    return [
        *tiles_between((10, 216, 417), (10, 218, 420)),  # 12 tiles, ~240KB
        *tiles_between((11, 433, 836), (11, 436, 839)),  # 16 tiles, ~320KB
        *tiles_between((12, 867, 1673), (12, 872, 1678)),  # 36 tiles, ~720KB (20km radius)
        *tiles_between((13, 1735, 3347), (13, 1744, 3357)),   # 110 tiles, ~2200KB (20km radius)
        *tiles_between((14, 3473, 6697), (14, 3487, 6711)),   # 225 tiles, ~4500KB (15km radius)
        *tiles_between((15, 6951, 13399), (15, 6970, 13418)),   # 400 tiles, ~8000KB (10km radius)
        # Total: 799 tiles, ~15.98MB
    ]


def get_irec_midland_tiles():
    """
        List of tiles for IREC Midland (Texas).
        (32.00592, -102.09694)
        Zoom level 10 to 15.

        https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1&mlat=32.00592&mlon=-102.09694#11/32.00592/-102.09694
    """
    return [
        *tiles_between((10, 220, 415), (10, 222, 416)),  # 6 tiles, ~120KB
        *tiles_between((11, 441, 830), (11, 444, 832)),  # 12 tiles, ~240KB
        *tiles_between((12, 884, 1661), (12, 887, 1664)),  # 16 tiles, ~320KB
        *tiles_between((13, 1769, 3324), (13, 1774, 3327)),   # 24 tiles, ~480KB
        *tiles_between((14, 3540, 6649), (14, 3548, 6654)),   # 54 tiles, ~1080KB
        *tiles_between((15, 7081, 13301), (15, 7095, 13309)),   # 135 tiles, ~2700KB
        # Total: 247 tiles, ~4.94MB
    ]


def get_launch_canada_base_tiles():
    """
        List of base tiles for Launch Canada (Timmins).
        Zoom level 6 to 9.
    """
    return [
        *tiles_between((6, 16, 21), (6, 18, 22)),  # 6 tiles, ~120KB
        *tiles_between((7, 33, 43), (7, 35, 44)),  # 6 tiles, ~120KB
        *tiles_between((8, 68, 88), (8, 70, 89)),  # 6 tiles, ~120KB
        *tiles_between((9, 138, 176), (9, 140, 178)),  # 9 tiles, ~180KB
        # Total: 27 tiles, ~0.54MB
    ]


def get_launch_canada_launchsite_tiles():
    """
        List of tiles for Launch Canada launch site.
        (47.9868850, -81.8484030)
        Zoom level 10 to 15.

        https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1&mlat=47.9868850&mlon=-81.8484030#12/47.9868850/-81.8484030
    """
    return [
        *tiles_between((10, 278, 355), (10, 279, 356)),  # 4 tiles, ~120KB
        *tiles_between((11, 557, 710), (11, 559, 713)),  # 12 tiles, ~240KB
        *tiles_between((12, 1114, 1422), (12, 1118, 1426)),  # 25 tiles, ~500KB (15km radius)
        *tiles_between((13, 2228, 2844), (13, 2237, 2853)),  # 100 tiles, ~2000KB (15km radius)
        *tiles_between((14, 4460, 5690), (14, 4472, 5703)),  # 182 tiles, ~3640KB (10km radius)
        *tiles_between((15, 8926, 11387), (15, 8939, 11399)),  # 182 tiles, ~3640KB (5km radius)
        # Total: 505 tiles, ~10.1MB
    ]


def get_launch_canada_timmins_tiles():
    """
        List of tiles for Launch Canada Timmins.
        (48.476455, -81.337474)
        Zoom level 10 to 15.

        https://tools.geofabrik.de/map/?type=Geofabrik_Standard&grid=1&mlat=48.476455&mlon=-81.337474#12/48.4765/-81.3375
    """
    return [
        *tiles_between((10, 279, 353), (10, 280, 354)),  # 4 tiles, ~80KB
        *tiles_between((11, 560, 707), (11, 561, 708)),  # 4 tiles, ~80KB
        *tiles_between((12, 1121, 1414), (12, 1123, 1416)),  # 9 tiles, ~180KB
        *tiles_between((13, 2242, 2830), (13, 2246, 2832)),   # 15 tiles, ~300KB
        *tiles_between((14, 4484, 5660), (14, 4492, 5665)),   # 54 tiles, ~1080KB
        *tiles_between((15, 8969, 11321), (15, 8984, 11330)),   # 160 tiles, ~3200KB
        # Total: 246 tiles, ~4.92MB
    ]


if __name__ == "__main__":
    download_tiles(
        get_north_america_base_tiles(),
        "./.tiles/na_base"
    )
    download_tiles(
        get_ulaval_tiles(),
        "./.tiles/ulaval"
    )
    # download_tiles(
    #     get_spaceport_launchsite_tiles(),
    #     "./.tiles/sac_launchsite"
    # )
    download_tiles(
        get_irec_base_tiles(),
        "./.tiles/irec_base"
    )
    download_tiles(
        get_irec_launchsite_tiles(),
        "./.tiles/irec_launchsite"
    )
    download_tiles(
        get_irec_midland_tiles(),
        "./.tiles/irec_midland"
    )
    download_tiles(
        get_launch_canada_base_tiles(),
        "./.tiles/lc_base"
    )
    download_tiles(
        get_launch_canada_launchsite_tiles(),
        "./.tiles/lc_launchsite"
    )
    download_tiles(
        get_launch_canada_timmins_tiles(),
        "./.tiles/lc_timmins"
    )
