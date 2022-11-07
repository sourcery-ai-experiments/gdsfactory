import gdsfactory as gf

a = gf.components.bbox(bbox=[(0, 0), (1, 2)])
b = gf.components.bbox(bbox=[(0, 0.5), (1, 1.5)])
d = gf.geometry.boolean(a, b, operation="not")

# s = set(id(p.properties) for p in d.polygons)
# print(s)

# d.polygons[0].properties["a"] = 1
# print(d.polygons[1].properties)

d.polygons[0].properties.append(1)
print(d.polygons[0].properties)
print(d.polygons[1].properties)
d.show()
