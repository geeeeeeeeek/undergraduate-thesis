import React, {PureComponent} from 'react';

import {BottomNavigation, BottomNavigationItem} from 'material-ui/BottomNavigation';
import Paper from 'material-ui/Paper';

import Explore from 'material-ui/svg-icons/action/explore';
import Layers from 'material-ui/svg-icons/maps/layers';
import Settings from 'material-ui/svg-icons/action/settings';

const discoverIcon = <Explore/>;
const mapIcon = <Layers/>;
const settingsIcon = <Settings/>;

export default class BottomNavigationBar extends PureComponent {
  render() {
    const {onViewChange, selectedIndex} = this.props;
    return (
      <Paper zDepth={1}>
        <BottomNavigation selectedIndex={selectedIndex}>
          <BottomNavigationItem
            label="地图"
            icon={mapIcon}
            onTouchTap={() => {onViewChange(0)}}
          />
          <BottomNavigationItem
            label="发现"
            icon={discoverIcon}
            onTouchTap={() => {onViewChange(1)}}
          />
          <BottomNavigationItem
            label="设置"
            icon={settingsIcon}
            onTouchTap={() => {onViewChange(2)}}
          />
        </BottomNavigation>
      </Paper>
    );
  }
}