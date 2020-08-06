import React, { Component } from 'react';
// import PropTypes from 'prop-types';

// Style
import '../static/styles/FoodieVenture.css'

export class FoodCategory extends Component { // Style function
    state = {
        opacity: 0.5,
    }

    getStyle = () => {
        return {
            borderRadius: "50%",
            width: 100,
            height: 100,
            transition: 0.3,
            opacity: this.state.opacity,
        }
    }

    buttonOnClick = () => {
        switch (this.props.name) {
            case 'breakfast':
                this.props.setFoodCategoryState('breakfast')
                this.setState({ opacity: (this.state.opacity === 1 ? 0.5 : 1) });
                break;
            case 'lunch':
                this.props.setFoodCategoryState('lunch')
                this.setState({ opacity: (this.state.opacity === 1 ? 0.5 : 1) });
                break;
            case 'dinner':
                this.props.setFoodCategoryState('dinner')
                this.setState({ opacity: (this.state.opacity === 1 ? 0.5 : 1) });
                break;
            case 'dessert':
                this.props.setFoodCategoryState('dessert')
                this.setState({ opacity: (this.state.opacity === 1 ? 0.5 : 1) });
                break;
            case 'coffee':
                this.props.setFoodCategoryState('coffee')
                this.setState({ opacity: (this.state.opacity === 1 ? 0.5 : 1) });
                break;
            case 'milkTea':
                this.props.setFoodCategoryState('milkTea')
                this.setState({ opacity: (this.state.opacity === 1 ? 0.5 : 1) });
                break;
            default:
                console.log("Button name not recognized")
        }
    }

    renderButton = () => {
        return (
            <div className="ButtonContainer">
                <input
                    type="image"
                    src={this.props.img}
                    alt="Submit"
                    className="Button"
                    style={this.getStyle()}
                    onClick={this.buttonOnClick}
                    name={this.props.name} />
            </div>

        )
    }

    render() {
        return this.renderButton();
    }
}

// PropTypes
// FoodCategory.propTypes = {
//     foodCategory: PropTypes.object.isRequired
// }

export default FoodCategory;
