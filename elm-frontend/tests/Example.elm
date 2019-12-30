module Example exposing (..)

import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, int, list, string)
import Test exposing (..)

import Utils exposing (..)

suite : Test
suite =
  describe "The Utils module"
    [ describe "Utils.capitalize"
      [ test "First letter is capitalized" <|
        \_ ->
          "abc"
            |> capitalize
            |> Expect.equal "Abc"
      , test "Single letter works fine" <|
        \_ ->
          "a"
            |> capitalize
            |> Expect.equal "A"
      , test "Empty string works fine" <|
        \_ ->
          ""
            |> capitalize
            |> Expect.equal ""
      , test "Doesn't mess with other capitals" <|
        \_ ->
          "abCDe"
            |> capitalize
            |> Expect.equal "AbCDe"
      , test "Doesn't mess with other words" <|
        \_ ->
          "abe fghi"
            |> capitalize
            |> Expect.equal "Abe fghi"
      ]
    ]

