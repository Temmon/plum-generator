module Endpoints exposing (..)

import Json.Decode exposing (Decoder, field, string, list)
import Json.Decode.Pipeline exposing (required)



type Model = String