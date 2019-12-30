module Utils exposing (..)

capitalize : String -> String
capitalize s =
  case ( String.uncons s ) of 
    Just (head, tail) -> 
      String.cons ( Char.toUpper head ) tail
    Nothing -> s
