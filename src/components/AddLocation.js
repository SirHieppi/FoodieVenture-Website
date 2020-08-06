import React, { Component } from 'react';
import Button from 'react-bootstrap/Button'
// import PropTypes from 'prop-types';

export class AddLocation extends Component {
    state = {
        location: '',
        url: "https://howardlam546.pythonanywhere.com",
    }

    getStyle = () => {
        return {
            padding: 25,
            flex: 2
        }
    }

    onChange = (e) => {
        this.setState({ location: e.target.value });
    }

    onSubmit = (e) => {
        if (this.state.location !== '') {
            this.props.setLocation(this.state.location);
            this.props.switchToState("selection");
            fetch((this.state.url + '/guest/new'), {
                method: 'POST',

                body: JSON.stringify({



                })
            })
                .then(response => response.json())
                .then(requestJSON => this.saveResults(requestJSON))

        } else {
            console.log("Location was not selected!");
        }
    }

    saveResults = (requestJSON) => {
        this.props.setUserID(requestJSON['guestID'])
    }

    render() {
        return (
            <form onSubmit={this.onSubmit}>
                <input
                    type='text'
                    placeholder='Location'
                    value={this.state.location}
                    onChange={this.onChange} >
                </input>

                <Button
                    type='submit'
                    value='Submit'
                    variant='success'
                    onClick={this.onSubmit}
                >
                    Proceed
                </Button>
            </form >
        )
    }
}


export default AddLocation;