import React, { Component } from 'react';

export class Footer extends Component {
    getStyle = () => {
        return {
            backgroundColor: '#FF9382',
            width: '100%',
            height: '10%',
            bottom: '0%',
            paddingBottom: '5%',
            position: 'fixed',
        }
    }

    render() {
        return (
            <div style={this.getStyle()}>

            </div>
        )
    }
}


export default Footer;