import React, { Component } from 'react';
// import Button from 'react-bootstrap/Button'

// Style
import '../static/styles/GeneratedPlace.css'

// Static Yelp Logo
import yelpBurstIcon from '../static/yelp_burst_icon.png';

// Static Yelp Stars
import zeroYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_0.png';
import oneYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_1.png';
import oneHalfYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_1_half.png';
import twoYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_2.png';
import twoHalfYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_2_half.png';
import threeYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_3.png';
import threeHalfYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_3_half.png';
import fourYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_4.png';
import fourHalfYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_4_half.png';
import fiveYelpStars from '../static/yelp_stars/web_and_ios/regular/regular_5.png';
import Button from 'react-bootstrap/Button';

export class GeneratedPlace extends Component {
    state = {

    }

    getStyle = () => {
        return {

        }
    }

    startOver = () => {
        this.props.switchToState("initial");
    }

    chooseImage = (rating) => {
        switch (rating) {
            case 0:
                return zeroYelpStars;
            case 1:
                return oneYelpStars;
            case 1.5:
                return oneHalfYelpStars;
            case 2:
                return twoYelpStars;
            case 2.5:
                return twoHalfYelpStars;
            case 3:
                return threeYelpStars;
            case 3.5:
                return threeHalfYelpStars;
            case 4:
                return fourYelpStars;
            case 4.5:
                return fourHalfYelpStars;
            case 5:
                return fiveYelpStars;
            default:
                return zeroYelpStars;

        }
    }

    capitalizeWord = (str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    render() {
        return (
            <div className="PlaceContainer">
                <div className="PlaceInfoContainer">
                    {/* <h2>
                        For {this.props.data.category}:
                    </h2> */}

                    <h3 className="PlaceName">
                        {this.capitalizeWord(this.props.data.category)}: {this.props.data.name}
                    </h3>

                    <div className="YelpInfoContainer">
                        <div className="YelpReviewNum">
                            {this.props.data.reviewNum} reviews
                        </div>
                        <div className="YelpStars">
                            <img src={this.chooseImage(this.props.data.rating)} alt=""></img>
                        </div>
                        <Button className="YelpLink">
                            <a href={this.props.data.url}>
                                <img src={yelpBurstIcon} alt=""></img>
                            </a>
                        </Button>

                    </div>

                    <div className="PlaceLocation">
                        {this.props.data.location}
                    </div>
                </div>

                <div className="PlaceImage">
                    <center>
                        <img
                            src={this.props.data.image_url}
                            alt="">
                        </img>
                    </center>
                </div>
            </div >
        )
    }
}

export default GeneratedPlace;


