import React, {Component} from 'react';

import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';

import Search from 'material-ui/svg-icons/action/search';
import {grey500, grey900} from 'material-ui/styles/colors';

const style = {
  Paper: {
    padding: '30px 20px 10px',
    display: 'flex',
    alignItems: 'center',
    flexShrink: 0,
    zIndex: 1
  },
  Search: {
    color: grey500,
    marginRight: '10px'
  },
  hintStyle: {
    color: grey500
  },
  underlineStyle: {
    display: 'none'
  }
}

export default class SearchBar extends Component {
  constructor(state, props) {
    super(state, props);
    this.state = {
      searchText: ''
    };
  }

  shouldComponentUpdate(nextProps, nextState) {
    return false;
  }

  handleTextChange(event, value) {
    this.setState({searchText: value});
  }

  render() {
    const {onTextChange} = this.props;
    return (
      <Paper zDepth={1} style={style.Paper}>
        <Search style={style.Search}/>
        <TextField
          hintText="想去哪里？"
          fullWidth={true}
          onChange={this.handleTextChange.bind(this)}
          onKeyPress={(e) => onTextChange(e, this.state.searchText)}
          hintStyle={style.hintStyle}
          underlineStyle={style.underlineStyle}/>
      </Paper>
    );
  }
}