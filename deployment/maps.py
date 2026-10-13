import folium


m = folium.Map(
    location=[50.7256, -3.5327], 
    zoom_start=13
    )
quickhull_coords = [
    [50.7350, -3.5400],
    [50.7300, -3.5150],
    [50.7150, -3.5200],
    [50.7200, -3.5500]
]

folium.Polygon(
    locations=quickhull_coords,
    fill=True,
    color="#ad644e",
    fill_color="#4e97ad",
    fill_opacity=0.3,
    popup="Region Info",
    tooltip="Hover for Info"
).add_to(m)

m.save("index.html")