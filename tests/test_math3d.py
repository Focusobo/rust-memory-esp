from esp_core.utils.math3d import Vec3


def test_vec_length() -> None:
    assert Vec3(3, 4, 0).length() == 5.0


def test_lerp_midpoint() -> None:
    a, b = Vec3(0, 0, 0), Vec3(10, 10, 10)
    assert a.lerp(b, 0.5) == Vec3(5, 5, 5)