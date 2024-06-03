import pytest
from gamepass.project import validate_user_option
from gamepass.project import validate_user_search
from gamepass.project import get_link
from gamepass.project import compare_search_and_game_list
from gamepass.project import generate_option_output
from gamepass.project import generate_result_output

def test_validate_user_option():
    assert validate_user_option("1") == "1"

def test_validate_user_option_1_spaces():
    assert validate_user_option("  1  ") == "1"

def test_validate_user_option_2():
    assert validate_user_option("2") == "2"

def test_validate_user_option_2_spaces():
    assert validate_user_option("  2  ") == "2"

def test_validate_user_option3():
    with pytest.raises(SystemExit):
        validate_user_option("3")

def test_validate_user_option3_spaces():
    with pytest.raises(SystemExit):
        validate_user_option("  3  ")

def test_validate_user_search():
    assert validate_user_search("Hero") == ["Hero"]

def test_validate_user_search_multiple():
    assert validate_user_search("Hero Friend DOOM") == ["Hero", "Friend", "DOOM"]

def test_get_link():
    assert get_link("1") == "https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=en-us&market=US"

def test_get_link_option2():
    assert get_link("2") == "https://catalog.gamepass.com/sigls/v2?id=fdd9e2a7-0fee-49f6-ad69-4354098401ff&language=en-us&market=US"

def test_compare_search_and_game_list():
    assert compare_search_and_game_list(["hero"], ["Human Fall Flat", "Humanity", "HUMANKIND"]) == []

def test_compare_search_and_game_list_exact_match_lower():
    assert compare_search_and_game_list(["human", "fall", "flat"], ["Human Fall Flat", "Humanity", "HUMANKIND"]) == ["Human Fall Flat"]

def test_compare_search_and_game_list_exact_match_upper():
    assert compare_search_and_game_list(["HUMAN", "Fall", "FlAt"], ["Human Fall Flat", "Humanity", "HUMANKIND"]) == ["Human Fall Flat"]

def test_compare_search_and_game_list_multiple_match_lower():
    assert compare_search_and_game_list(["human"], ["Human Fall Flat", "Humanity", "HUMANKIND"]) == ["Human Fall Flat", "Humanity", "HUMANKIND"]

def test_compare_search_and_game_list_multiple_match_upper():
    assert compare_search_and_game_list(["HuMaN"], ["Human Fall Flat", "Humanity", "HUMANKIND"]) == ["Human Fall Flat", "Humanity", "HUMANKIND"]

def test_generate_option_output():
    assert generate_option_output("1") == "For Game Pass games available on Console:"

def test_generate_option_output_option_2():
    assert generate_option_output("2") == "For Game Pass games available on PC:"

def test_generate_result_output():
    assert generate_result_output(["hero"], []) == "No Matches Found"

def test_generate_result_output_one_match_exact():
    assert generate_result_output(["HUMAN", "Fall", "FlAt"], ["Human Fall Flat"]) == "Found An Exact Match! 'Human Fall Flat' is on the list of available games."

def test_generate_result_output_one_match_nonexact():
    assert generate_result_output(["HuMaN"], ["Human Fall Flat"]) == "No Exact Match. However, 'Human Fall Flat' is on the list of available games."

def test_generate_result_output_one_match_multiple():
    assert generate_result_output(["HuMaN"], ["Human Fall Flat", "Humanity", "HUMANKIND"]) == "No Exact Match. However, here is a list of games close to your search:\n"
