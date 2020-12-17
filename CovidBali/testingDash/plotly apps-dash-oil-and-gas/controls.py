
# In[]:
# Controls for webapp
import numpy as np

## since fitbounds='location not working
# from https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
## NOT WORKING ! zoom and center defined in if clause

def zoom_center(lons: tuple=None, lats: tuple=None, lonlats: tuple=None,
        format: str='lonlat', projection: str='mercator',
        width_to_height: float=2.0) -> (float, dict):
    """Finds optimal zoom and centering for a plotly mapbox.
    Must be passed (lons & lats) or lonlats.
    Temporary solution awaiting official implementation, see:
    https://github.com/plotly/plotly.js/issues/3434
    
    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    lonlats: tuple, optional, gps locations
    format: str, specifying the order of longitud and latitude dimensions,
        expected values: 'lonlat' or 'latlon', only used if passed lonlats
    projection: str, only accepting 'mercator' at the moment,
        raises `NotImplementedError` if other is passed
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.
    
    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys

    >>> print(zoom_center((-109.031387, -103.385460),
    ...     (25.587101, 31.784620)))
    (5.75, {'lon': -106.208423, 'lat': 28.685861})
    """
    if lons is None and lats is None:
        if isinstance(lonlats, tuple):
            lons, lats = zip(*lonlats)
        else:
            raise ValueError(
                'Must pass lons & lats or lonlats'
            )
    
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }
    
    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])
    
    if projection == 'mercator':
        margin = 1.2
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)
    else:
        raise NotImplementedError(
            f'{projection} projection is not implemented'
        )
    
    return zoom, center
    
REGENCIES = dict(
    JE = 'Jembrana',
    BA = 'Badung',
    DE = 'Kota Denpasar',
    BU = 'Buleleng',
    KL = 'Klungung'
    TA = 'Tabanan',
    GI = 'Gianyar',
    KA = 'Karangasem',
    BA = 'Bangli'
    )

COUNTIES = {
    "001": "Albany",
    "003": "Allegany",
    "005": "Bronx",
    "007": "Broome",
    "009": "Cattaraugus",
    "011": "Cayuga",
    "013": "Chautauqua",
    "015": "Chemung",
    "017": "Chenango",
    "019": "Clinton",
    "021": "Columbia",
    "023": "Cortland",
    "025": "Delaware",
    "027": "Dutchess",
    "029": "Erie",
    "031": "Essex",
    "033": "Franklin",
    "035": "Fulton",
    "037": "Genesee",
    "039": "Greene",
    "041": "Hamilton",
    "043": "Herkimer",
    "045": "Jefferson",
    "047": "Kings",
    "049": "Lewis",
    "051": "Livingston",
    "053": "Madison",
    "055": "Monroe",
    "057": "Montgomery",
    "059": "Nassau",
    "061": "New York",
    "063": "Niagara",
    "065": "Oneida",
    "067": "Onondaga",
    "069": "Ontario",
    "071": "Orange",
    "073": "Orleans",
    "075": "Oswego",
    "077": "Otsego",
    "079": "Putnam",
    "081": "Queens",
    "083": "Rensselaer",
    "085": "Richmond",
    "087": "Rockland",
    "089": "St. Lawrence",
    "091": "Saratoga",
    "093": "Schenectady",
    "095": "Schoharie",
    "097": "Schuyler",
    "099": "Seneca",
    "101": "Steuben",
    "103": "Suffolk",
    "105": "Sullivan",
    "107": "Tioga",
    "109": "Tompkins",
    "111": "Ulster",
    "113": "Warren",
    "115": "Washington",
    "117": "Wayne",
    "119": "Westchester",
    "121": "Wyoming",
    "123": "Yates",
}

WELL_STATUSES = dict(
    AC="Active",
    AR="Application Received to Drill/Plug/Convert",
    CA="Cancelled",
    DC="Drilling Completed",
    DD="Drilled Deeper",
    DG="Drilling in Progress",
    EX="Expired Permit",
    IN="Inactive",
    NR="Not Reported on AWR",
    PA="Plugged and Abandoned",
    PI="Permit Issued",
    PB="Plugged Back",
    PM="Plugged Back Multilateral",
    RE="Refunded Fee",
    RW="Released - Water Well",
    SI="Shut-In",
    TA="Temporarily Abandoned",
    TR="Transferred Permit",
    UN="Unknown",
    UL="Unknown Located",
    UM="Unknown Not Found",
    VP="Voided Permit",
)

WELL_TYPES = dict(
    BR="Brine",
    Confidential="Confidential",
    DH="Dry Hole",
    DS="Disposal",
    DW="Dry Wildcat",
    GD="Gas Development",
    GE="Gas Extension",
    GW="Gas Wildcat",
    IG="Gas Injection",
    IW="Oil Injection",
    LP="Liquefied Petroleum Gas Storage",
    MB="Monitoring Brine",
    MM="Monitoring Miscellaneous",
    MS="Monitoring Storage",
    NL="Not Listed",
    OB="Observation Well",
    OD="Oil Development",
    OE="Oil Extension",
    OW="Oil Wildcat",
    SG="Stratigraphic",
    ST="Storage",
    TH="Geothermal",
    UN="Unknown",
)

WELL_COLORS = dict(
    GD="#FFEDA0",
    GE="#FA9FB5",
    GW="#A1D99B",
    IG="#67BD65",
    OD="#BFD3E6",
    OE="#B3DE69",
    OW="#FDBF6F",
    ST="#FC9272",
    BR="#D0D1E6",
    MB="#ABD9E9",
    IW="#3690C0",
    LP="#F87A72",
    MS="#CA6BCC",
    Confidential="#DD3497",
    DH="#4EB3D3",
    DS="#FFFF33",
    DW="#FB9A99",
    MM="#A6D853",
    NL="#D4B9DA",
    OB="#AEB0B8",
    SG="#CCCCCC",
    TH="#EAE5D9",
    UN="#C29A84",
)
