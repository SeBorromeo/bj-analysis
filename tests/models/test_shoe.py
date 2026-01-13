import pytest
from models.shoe import Shoe
from models.card import Card

def test_shoe_size_and_shuffle_card():
    num_decks = 6
    shoe = Shoe(num_decks)

    total_cards = 52 * num_decks
    expected_size = total_cards  # burn 1, insert 1

    assert len(shoe.shoe) == expected_size
    assert shoe.shoe.count("shuffle_card") == 1


def test_shuffle_card_position():
    shoe = Shoe(6)

    idx = shoe.shoe.index("shuffle_card")
    ratio = idx / len(shoe.shoe)

    assert 0.25 <= ratio <= 0.35


def test_shuffle_card_triggers_reshuffle(monkeypatch):
    shoe = Shoe(1)

    # Force shuffle card to top
    shoe.shoe = ["shuffle_card"] + shoe.shoe

    old_len = len(shoe.shoe)
    card = shoe.deal_card()

    assert isinstance(card, Card)
    assert len(shoe.shoe) < old_len  # reshuffled and dealt

