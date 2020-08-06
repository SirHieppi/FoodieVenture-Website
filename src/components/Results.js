import React, { Component } from 'react';
import Button from 'react-bootstrap/Button'
import GeneratedPlace from './GeneratedPlace.js';
import { Gallery, GalleryImage } from 'react-gesture-gallery'

// Style
import '../static/styles/results.css'

export class Results extends Component {
    componentDidMount() {
        this.getPlaces();
    }

    state = {
        opacity: 0.5,
        requestJSON: [],
        categories: [],
        url: "https://howardlam546.pythonanywhere.com",
        imageIndex: 0
    }

    startOver = () => {
        this.props.removeCurrentGuest();
        this.props.switchToState("initial");
    }

    getPlaces = () => {
        fetch((this.state.url + ('/results/id/') + this.props.userID), {
            method: 'POST',
            // headers: {
            //     'Accept': 'application/json',
            //     'Content-Type': 'application/json',
            // },
            body: JSON.stringify({
                location: this.props.location,
                selectedFoodCategories: this.props.selectedFoodCategories,
            })
        })
            .then(response => response.json())
            .then(requestJSON => this.updateResults(requestJSON));
    }

    updateResults = (requestJSON) => {
        this.setState({ requestJSON: requestJSON })
    }

    reselectCategories = () => {
        this.props.switchToState("selection");
    }

    renderPlace = (j) => {
        console.log(j)

        return (
            <div>
                {j.name}
            </div>
        )
    }

    render() {
        return (
            <div className="ResultsContainer">
                <center>
                    Generating FoodieVenture near {this.props.location}...
                </center>

                <div className="PlacesContainer">
                    <Gallery
                        index={this.state.imageIndex}
                        onRequestChange={i => {
                            this.setState({ imageIndex: i });
                        }}
                    >
                        {this.state.requestJSON.map((category, index) => (
                            <GeneratedPlace key={index} data={category} />
                        ))}
                    </Gallery>
                    {/* {this.state.requestJSON.map((category, index) => (
                        <GeneratedPlace key={index} data={category} />
                    ))} */}
                </div>

                <div className="UserOptionsContainer">
                    <Button className="Refresh" variant="light" onClick={this.getPlaces}>Refresh</Button>
                    <Button className="ReselectCategories" variant="light" onClick={this.reselectCategories}>Reselect</Button>
                    <Button className="StartOver" variant="light" onClick={this.startOver}>Restart</Button>
                </div>
            </div>
        )
    }
}

export default Results;


