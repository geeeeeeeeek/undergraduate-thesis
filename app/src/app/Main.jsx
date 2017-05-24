/**
 * In this file, we create a React component
 * which incorporates components provided by Material-UI.
 */
import React, {Component} from 'react';

import {deepOrange500} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import DiscoverView from './views/DiscoverView/DiscoverView.jsx';
import SettingsView from './views/SettingsView/SettingsView.jsx';
import VisualizationView from './views/VisualizationView/VisualizationView.jsx';
import ParkDetailsView from './views/DiscoverView/ParkDetailsView.jsx';

import BottomNavigationBar from './components/BottomNavigationBar.jsx';

const muiTheme = getMuiTheme({
  palette: {
    accent1Color: deepOrange500
  }
});

const appStyle = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    justifyContent: 'space-between'
  },
  viewContainer: {
    display: 'flex',
    flexDirection: 'column',
    overflowX: 'hidden'
  },
  bottomNavigationBar: {
    alignSelf: 'flex-end'
  }
}

class Main extends Component {
  constructor(state, props) {
    super(state, props);
    this.state = {
      viewId: 1
    };
    this.activeInfoObject = null;
  }

  handleViewChange(viewId) {
    this.setState({viewId: viewId});
  }

  getActiveView() {
    const {viewId} = this.state;

    let infoObject = null;

    switch (viewId) {
      case 0:
        return (<VisualizationView/>);
      case 1:
        return (<DiscoverView
          onDetailsViewOpen={(info) => {
          this.activeInfoObject = info;            
          this.handleViewChange(4);
        }}/>);
      case 2:
        return (<SettingsView/>);
      case 4:
        return (<ParkDetailsView
          info={this.activeInfoObject}
          onDetailsViewClose={() => {
          this.handleViewChange(1)
        }}/>);
    }
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <div style={appStyle.container}>
          <div style={appStyle.viewContainer}>
            {this.getActiveView()}
          </div>
          <BottomNavigationBar
            style={appStyle.bottomNavigationBar}
            selectedIndex={this.state.viewId % 3}
            onViewChange={this.handleViewChange.bind(this)}/>
        </div>
      </MuiThemeProvider>
    );
  }
}

export default Main;
