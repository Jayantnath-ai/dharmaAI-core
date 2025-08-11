from dharma_core import load_scrolls, iter_simulations, list_artifacts

def test_scrolls_present():
    # Doesn’t assert content; just verifies packaging works
    _ = load_scrolls()

def test_simulations_iter():
    _ = list(iter_simulations())

def test_listing():
    listing = list_artifacts()
    assert isinstance(listing, dict)
