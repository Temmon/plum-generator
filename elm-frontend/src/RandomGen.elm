import Browser
--import Html exposing (..)
--import Html.Attributes exposing (..)
--import Html.Events exposing (onClick)
import Http
import Json.Decode exposing (Decoder, field, string, list)
import Json.Decode.Pipeline exposing (required)
import Utils exposing (capitalize)
import Url.Builder as Url exposing (absolute)
import Browser exposing (Document)

import Element exposing (..)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Element.Input as Input exposing (button)
--import Endpoints exposing (getEndpoints)



-- MAIN


main =
  Browser.document
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }



-- MODEL


type Status
  = Failure
  | Loading
  | Loaded
  | Waiting

type alias Model =
  { endpoints: List String  
  , result: RandomResult
  , status: Status
  }

type alias Endpoints =
  (List String)


type alias RandomResult = 
  { name: String
  , data: List (List String)
  }


init : () -> (Model, Cmd Msg)
init _ =
  (
  { endpoints = []
  , result = { name = "none", data = [] }
  , status = Waiting
  }, 
  getEndpoints)


-- UPDATE


type Msg
  = MorePlease String
  | GotEndpoints (Result Http.Error Endpoints)
  | GotData (Result Http.Error RandomResult)
  | Empty


update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    MorePlease endpoint ->
      ( model, getData endpoint)

    GotData result ->
      case result of
        Ok data ->
          ( { model | status = Loaded, result = data }, Cmd.none )

        Err _ ->
          ( { model | status = Failure }, Cmd.none)   

    GotEndpoints result ->
      case result of
        Ok data ->
          ( { model | status = Waiting, endpoints = data } , Cmd.none)

        Err _ ->
          ( { model | status = Failure }, Cmd.none)

    Empty -> (model, Cmd.none)



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- VIEW





view: Model -> Document Msg
view model = 
  let 
    edges =
      { top = 0
      , right = 0
      , bottom = 0
      , left = 0
      }

    scaled = Element.modular 16 1.25
  in 
    { title = "Plum good generators"
    , body = [ Element.layout [ Background.color (rgb255 230 230 250)] 
      <|
        Element.column  [ width (px 800)
                        , height fill
                        , centerX
                        , spacing 36
                        , paddingEach { edges | top = 50 }
          --              , Background.color (rgb255 150 150 150)
                        ]
          [ Element.paragraph [ Font.size ( floor (scaled 4) ) ] [ Element.text "Plum Good Generators" ]
          , case model.endpoints of 
            [] -> Element.none
            _ -> Element.wrappedRow [] ( List.map 
                ( \e -> Input.button [ padding 10 ] 
                  { onPress = Just (MorePlease e)
                  , label = text (capitalize e) 
                  } ) 
                model.endpoints )
          , case model.status of
            Loaded -> Element.column  [ spacing 15 
                                      , paddingEach { edges | left=10 }
                                      ] 
                                      ( List.map makeParagraph model.result.data )
            Failure -> Element.text "Failed to get data"
            _ -> Element.none
          ]
      ]
  }   

makeParagraph : (List String) -> Element msg
makeParagraph data = Element.column [ spacing 5 ] (List.map ( \e ->  ( showList e ) ) data)

showList : String -> Element msg
showList data = Element.paragraph [] [ Element.text (capitalize data) ]





-- HTTP

getData : String -> Cmd Msg
getData endpoint = 
  Http.get
    { url = Url.absolute [ "randomapi", endpoint, String.fromInt 5 ] []
    , expect = Http.expectJson GotData randomDecoder
    }


  
getEndpoints : Cmd Msg
getEndpoints =
  Http.get
    { url = Url.absolute [ "randomapi", "randomizers" ] []
    , expect = Http.expectJson GotEndpoints endpointDecoder }

endpointDecoder : Decoder Endpoints
endpointDecoder =
  (list string)
    

randomDecoder : Decoder RandomResult
randomDecoder =
  Json.Decode.succeed RandomResult
    |> required "name" string
    |> required "data" (list (list string))


