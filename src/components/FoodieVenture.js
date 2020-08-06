import React, { Component } from 'react';
import FoodCategory from './FoodCategory';
// import PropTypes from 'prop-types';
import Button from 'react-bootstrap/Button'


// Static Button Images
import breakfastButtonImage from '../static/breakfastButtonImage.jpg';
import lunchButtonImage from '../static/lunchButtonImage.png';
import dinnerButtonImage from '../static/dinnerButtonImage.jpg';
import coffeeButtonImage from '../static/coffeeButtonImage.jpg';
import dessertButtonImage from '../static/dessertButtonImage.png';
import bobaButtonImage from '../static/bobaButtonImage.jpg';

// Style
import '../static/styles/FoodieVenture.css'

class FoodieVenture extends Component {
    state = {
        randomBool: true,
        selectedFoodCategories: [],
        breakfast: false,
    }

    buttons = () => {
        return (
            <div className="ButtonsContainer">
                <div className="rowOneContainer">
                    <FoodCategory
                        img={breakfastButtonImage}
                        name="breakfast"
                        selectedFoodCategories={this.selectedFoodCategories}
                        setFoodCategoryState={this.setFoodCategoryState} />

                    <FoodCategory
                        img={lunchButtonImage}
                        name="lunch"
                        selectedFoodCategories={this.selectedFoodCategories}
                        setFoodCategoryState={this.setFoodCategoryState} />

                    <FoodCategory
                        img={dinnerButtonImage}
                        name="dinner"
                        selectedFoodCategories={this.selectedFoodCategories}
                        setFoodCategoryState={this.setFoodCategoryState} />
                </div>

                <div className="rowTwoContainer">
                    <FoodCategory
                        img={dessertButtonImage}
                        name="dessert"
                        selectedFoodCategories={this.selectedFoodCategories}
                        setFoodCategoryState={this.setFoodCategoryState} />

                    <FoodCategory
                        img={coffeeButtonImage}
                        name="coffee"
                        selectedFoodCategories={this.selectedFoodCategories}
                        setFoodCategoryState={this.setFoodCategoryState} />

                    <FoodCategory
                        img={bobaButtonImage}
                        name="milkTea"
                        selectedFoodCategories={this.selectedFoodCategories}
                        setFoodCategoryState={this.setFoodCategoryState} />
                </div>
            </div>
        )
    }

    proceed = () => {
        console.log("Proceeding!");

        // No buttons have been selected
        if (this.state.selectedFoodCategories.length === 0) {
            console.log("No buttons have been selected!");
        } else {
            console.log("Generating food adventure!");
            this.props.switchToState("result");
            this.props.setSelectedFoodCategories(this.state.selectedFoodCategories);
        }
    }

    checkSelectedCategoryState = (categoryToCheck) => {
        for (var x = 0; x < this.state.selectedFoodCategories.length; x++) {
            if (categoryToCheck === this.state.selectedFoodCategories[x]) {
                return true;
            }
        }
        return false;
    }

    removeSelectedCategory = (category) => {
        this.setState({ selectedFoodCategories: this.state.selectedFoodCategories.filter(c => c !== category) })
    }

    addSelectedCategory = (category) => {
        this.setState({ selectedFoodCategories: this.state.selectedFoodCategories.concat(category) });
    }

    setFoodCategoryState = (foodCategory) => {
        if (this.checkSelectedCategoryState(foodCategory)) {
            this.removeSelectedCategory(foodCategory);
        } else {
            this.addSelectedCategory(foodCategory);
        }
    }

    render() {
        return (
            <div className="SelectionPageContainer">
                <center className="SelectionDescription">
                    Select categories to generate your very own FoodieVenture!
            </center>
                <div className="SelectionButtons">
                    {this.buttons()}
                </div>

                <div className="ProceedButton">
                    <Button variant="success" onClick={this.proceed}>Proceed</Button>
                </div>
            </div >
        );
    }
}



// PropTypes
// FoodieVenture.propTypes = {
//     foodCategories: PropTypes.array.isRequired
// }

export default FoodieVenture;
