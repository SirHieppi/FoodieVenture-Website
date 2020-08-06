import React, { Component } from 'react';

export class Title extends Component {
    getStyle = () => {
        return {
            backgroundColor: '#FF9382',
            fontFamily: 'cursive',
            color: 'white',
            fontWeight: 'bold',
            width: 400,
        }
    }

    render() {
        return (
            <div style={this.getStyle()}>
                <center><h2>
                    FoodieVenture
                </h2></center>
            </div>
        )
    }
}


export default Title;