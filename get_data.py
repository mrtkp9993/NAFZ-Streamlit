import geopandas

data = geopandas.read_file("EFSM20_CF_PLD.geojson")
data = data[data.idsource.str.startswith("NAF")]  # north anatolian fault

coordinates = []
for i in range(data.shape[0]):
    coordinates.append(data["geometry"].iloc[i].bounds)

for c in coordinates:
    print(
        f"www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat={c[1]}&maxlat={c[3]}&minlon={c[0]}&maxlon={c[2]}&format=json&nodata=204&minmag=4"
    )
