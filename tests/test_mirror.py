import gdsfactory as gf


def test_mirror():
    c1 = gf.pcells.pad()
    c1.mirror()


if __name__ == "__main__":
    test_mirror()
