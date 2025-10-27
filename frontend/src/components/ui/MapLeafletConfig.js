import {
    polyline as Lpolyline,
    tileLayer as LtileLayer,
    icon as Licon,
    marker as Lmarker,
    featureGroup as LfeatureGroup,
    control as Lcontrol,
} from "leaflet";

const myIcons = {
    rocket: Licon({
        iconUrl: "/img/rocket.svg",
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, -10],
    }),
    userPos: Licon({
        iconUrl: "/img/user_pos.png",
        iconSize: [16, 16],
        iconAnchor: [8, 8],
        popupAnchor: [0, -8],
    }),
    launchpad: Licon({
        iconUrl: "/img/launchpad.png",
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, -10],
    }),
};

const LAUNCH_CANADA_LL = [47.986885, -81.848403];
// const SPACEPORT_AMERICA_LL = [32.9895, -106.97509];
const IREC_LL = [31.043707, -103.528598];

const myMarkers = {
    rocket: Lmarker([0, 0], { icon: myIcons.rocket }).bindPopup("<b>Rocket position</b>"),
    userPos: Lmarker([0, 0], { icon: myIcons.userPos }).bindPopup("<b>You're here</b>"),
    launchCanada: Lmarker(LAUNCH_CANADA_LL, { icon: myIcons.launchpad }).bindPopup("<b>Launch Canada !</b>"),
    // spacePortAmerica: Lmarker(SPACEPORT_AMERICA_LL, { icon: myIcons.launchpad }).bindPopup(
    //     "<b>Spaceport America !</b>"
    // ),
    irec: Lmarker(IREC_LL, { icon: myIcons.launchpad }).bindPopup("<b>IREC !</b>"),
};

// const myLaunchpadsLayer = LfeatureGroup([myMarkers.launchCanada, myMarkers.spacePortAmerica]);
const myLaunchpadsLayer = LfeatureGroup([myMarkers.launchCanada, myMarkers.irec]);

const myPolyline = Lpolyline([], { color: "grey" });

const myLocalTiles = LtileLayer("/tiles/{z}/{x}/{y}.png", {
    maxZoom: 15,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
});

const myOnlineTiles = LtileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
});

const myControlLayer = Lcontrol.layers(
    {
        Local: myLocalTiles,
        Online: myOnlineTiles,
    },
    {
        '<img src="/img/launchpad.png" alt="Launchpad Icon" width=20 height=20 />': myLaunchpadsLayer,
    },
    {
        collapsed: false,
    }
);

export { myIcons, myMarkers, myLaunchpadsLayer, myPolyline, myLocalTiles, myOnlineTiles, myControlLayer };
