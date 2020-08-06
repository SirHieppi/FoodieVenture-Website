// React
// import Button from 'react-bootstrap/Button'
import React, { Component } from 'react';

// Components
import FoodieVenture from './components/FoodieVenture.js';
import AddLocation from './components/AddLocation.js';
import Title from './components/Title.js';
import Footer from './components/Footer.js';
import Results from './components/Results.js';

// Styling
import './App.css';

class App extends Component {
    state = {
        // State = { initial, selection, result }
        currentState: "location",

        selectedFoodCategories: [],

        location: '',

        userID: -1,

        url: "https://howardlam546.pythonanywhere.com"
    }

    // Things to do before unloading/closing the tab
    doSomethingBeforeUnload = () => {
        if (this.state.userID !== -1) {
            this.removeCurrentGuest()
        }
    }

    // Setup the `beforeunload` event listener
    setupBeforeUnloadListener = () => {
        window.addEventListener("beforeunload", (ev) => {
            ev.preventDefault();
            return this.doSomethingBeforeUnload();
        });
    };

    componentDidMount() {
        // Activate the event listener
        this.setupBeforeUnloadListener();

        if (this.state.userID !== -1) {
            this.removeCurrentGuest()
        }
    }

    componentWillUnmount() {
        if (this.state.userID !== -1) {
            this.removeCurrentGuest()
        }
    }

    removeCurrentGuest = () => {
        console.log("making a request to " + ((this.state.url + '/guest/id/') + this.state.userID + '/remove'));
        fetch(((this.state.url + '/guest/id/') + this.state.userID + '/remove'), {
            method: 'POST',
            body: JSON.stringify({

            })
        })
    }

    setLocation = (l) => {
        //check valid location

        this.setState({ location: l, inInitialState: false });
        console.log("setting location");
        console.log(this.state.location);
    }

    setUserID = (uID) => {
        this.setState({ userID: uID });
    }

    setSelectedFoodCategories = (array) => {
        this.setState({ selectedFoodCategories: array })
    }

    // Application states

    // Let user select location for generation
    initialState = () => {
        return (
            <div className="AppContainerInitial">
                <div className="Title">
                    <Title className='title' />
                </div>

                <div className="AddLocation">
                    <AddLocation
                        setLocation={this.setLocation}
                        switchToState={this.switchToState}
                        userID={this.state.userID}
                        setUserID={this.setUserID} />
                </div>

                {/* <div className="FooterInitial">
                    <Footer />
                </div> */}
            </div>
        );
    }

    // Let user select categories
    selectionState = () => {
        return (
            <div className="AppContainerSelection">
                <div className="Title">
                    <Title />
                </div>

                <div className="FoodieVentureSelection">
                    <FoodieVenture
                        foodCategories={this.state.foodCategories}
                        selectButton={this.selectButton}
                        switchToState={this.switchToState}
                        setSelectedFoodCategories={this.setSelectedFoodCategories}
                        userID={this.state.userID}
                    />
                </div>

                {/* <div className="FooterSelection">
                    <Footer />
                </div> */}
            </div>);
    }

    resultsState = () => {
        return (
            <div className="AppContainerResults">
                <div className="Title">
                    <Title />
                </div>

                <div className="Results">
                    <Results
                        selectedFoodCategories={this.state.selectedFoodCategories}
                        switchToState={this.switchToState}
                        location={this.state.location}
                        userID={this.state.userID}
                        removeCurrentGuest={this.removeCurrentGuest} />
                </div>

                {/* <div className="FooterResults">
                    <Footer />
                </div> */}
            </div>
        )
    }

    storeDataInSessionStorage = (key, value) => {
        sessionStorage.setItem(key, value)
    }

    // Helper Functions

    switchToState = (state) => {
        switch (state) {
            case "initial":
                this.setState({ currentState: "initial" });
                break;
            case "selection":
                this.setState({ currentState: "selection" });
                break;
            case "result":
                this.setState({ currentState: "result" });
                break;
            default:
                this.setState({ currentState: "initial" });
        }
    }

    render() { // const { id, category } = this.props.foodCategories;
        console.log("Guest id is " + this.state.userID)

        switch (this.state.currentState) {
            case "initial":
                return this.initialState();
            case "selection":
                return this.selectionState();
            case "result":
                return this.resultsState();
            default:
                return this.initialState();
        }
    }
}

export default App;
