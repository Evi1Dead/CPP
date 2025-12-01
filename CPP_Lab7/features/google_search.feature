Feature: Google Search baseline (Variants 1-3)
  To satisfy Lab 7 we automate the Variant 1, Variant 2, and Variant 3 checks for
  Google Search using Cucumber BDD, Selenium, and Chrome.

  Background:
    Given I open the Google home page

  @variant1 @smoke
  Scenario: Page opens with key widgets present
    Then the page title should contain "Google"
    And the following elements should be visible
      | name              | locator_key             |
      | Search box        | home.search_box         |
      | Google Search btn | home.search_button      |
      | Lucky button      | home.feeling_lucky      |
    And the Google logo should be displayed

  @variant1
  Scenario: Count search results per page
    When I search for "test automation"
    Then at least 8 organic results should be shown
    And no more than 12 organic results should be shown

  @variant1
  Scenario: Blank submission should not trigger results
    When I submit an empty query
    Then I should remain on the Google home page
    And no results section should be visible

  @variant1
  Scenario: Typo search suggests a "Did you mean" correction
    When I search for "gogle tutorial"
    Then the "Did you mean" suggestion should be visible

  @variant2
  Scenario: Gibberish query shows no matches
    When I search for "++++++"
    Then I should see a no results message explaining there were no matches

  @variant2
  Scenario: Accepting a suggestion updates the query and results
    When I search for "gogle"
    And I accept the suggested correction
    Then the search box should contain "google"
    And at least 5 organic results should be shown

  @variant2
  Scenario: Autocomplete suggestions appear for partial keywords
    When I type "Tehnical" into the search box without submitting
    Then I should see autocomplete suggestions containing "technical"

  @variant3
  Scenario: Search supports other languages
    When I search for "привет мир"
    Then at least 3 organic results should be shown
    And the first organic result should contain "привет"

  @variant3
  Scenario: Google search is not case sensitive
    When I search for "selenium testing"
    And I store the first organic result title as "baseline_case"
    And I search for "SELENIUM TESTING"
    Then the first organic result title should match "baseline_case"

  @variant3
  Scenario: Calculator service appears for arithmetic queries
    When I search for "2+2"
    Then the calculator result should display "4"

  @variant3
  Scenario: Currency converter appears for conversion queries
    When I search for "100 usd to eur"
    Then the currency converter widget should be visible
