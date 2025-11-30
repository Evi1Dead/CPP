Feature: Mens catalog experience on Elite Shoppy
  The historical Lab 3 manual scenarios are automated end-to-end with Cucumber BDD,
  Selenium WebDriver, and Chrome. Known defects are intentionally asserted so that
  regressions remain visible.

  Background:
    Given I open the "mens" page

  @tc-men-001
  Scenario: TC-MEN-001 Page load and header integrity
    Then the page title should contain "Elite Shoppy"
    And no javascript errors should be present in the console
    And the product grid should contain at least 8 cards
    And the following elements should be visible:
      | element            | locator_key          |
      | Logo               | header.logo          |
      | Search form        | header.search        |
      | Navigation menu    | header.nav           |
      | Cart button        | header.cart_button   |
    And each header link should be reachable

  @tc-men-002
  Scenario: TC-MEN-002 Sorting control default and price ordering
    When I capture the current product prices
    And I sort products by option "Price(High - Low)"
    Then the captured prices should be sorted from high to low
    When I sort products by option "Price(Low - High)"
    Then the captured prices should be sorted from low to high

  @tc-men-003
  Scenario: TC-MEN-003 Product card content and navigation
    Then every product card should expose image title and price
    When I open the details page for the first product
    Then the PDP should load without rendering errors

  @tc-men-004
  Scenario: TC-MEN-004 Add to cart flow from catalog
    When I add the first product to the cart from the catalog
    Then the mini cart should display the product with quantity "1"

  @tc-men-005
  Scenario: TC-MEN-005 Update quantity and persistence in cart
    Given the mini cart already contains an item
    When I update the mini cart quantity to "2"
    And I refresh the mini cart view
    Then the mini cart quantity should persist as "2"

  @tc-men-006
  Scenario: TC-MEN-006 Negative quantity validation and overlay rules
    Given the mini cart already contains an item
    When I attempt to set the mini cart quantity to "-1"
    Then a validation error or warning should be displayed
    And the checkout button should remain disabled until values are valid
