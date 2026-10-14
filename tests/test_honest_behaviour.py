from sifa_mcp import main as server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_the_demo_profile_id_is_stable_and_the_phone_is_masked():
    a = _fn("create_worker_profile")("Test Person", "0700123456", "plumbing", "pipes", "Nairobi", 3, "Swahili")
    b = _fn("create_worker_profile")("Test Person", "0700123456", "plumbing", "pipes", "Nairobi", 3, "Swahili")
    assert a["profile_id"] == b["profile_id"] and "0700123456" not in str(a)
