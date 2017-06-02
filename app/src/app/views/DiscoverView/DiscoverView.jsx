import React, {Component} from 'react';

import {GridList, GridTile} from 'material-ui/GridList';
import IconButton from 'material-ui/IconButton';
import Subheader from 'material-ui/Subheader';

import PlaceIcon from 'material-ui/svg-icons/maps/place';
import CircularProgress from 'material-ui/CircularProgress';

import SearchBar from '../../components/SearchBar.jsx';

import POIInfoUtil from '../../utils/POIInfoUtil.jsx';

import {grey100} from 'material-ui/styles/colors';

const style = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        background: grey100
    },
    spinner: {
        marginTop: '40px',
        alignSelf: 'center'
    },
    gridList: {
        overflowY: 'auto'
    }
}

export default class DiscoverView extends Component {
    constructor(state, props) {
        super(state, props);
        this.state = {
            items: [],
            helperText: '为您推荐周围兴趣点',
            searching: false
        }
        this.poiInfoUtil = new POIInfoUtil();
    }

    componentDidMount() {
        this.getNearestList();
    }

    getNearestList() {
        this.setState({searching: true});
        this.poiInfoUtil.listNearest().then((items) => {
            this.setState({
                searching: false,
                items: items
            });
        });
    }

    handleSearchTextChange(e, searchText) {
        if (e.key === 'Enter') {
            this.handleSearch(searchText);
        }
    }

    handleSearch(searchText) {
        if (!searchText) {
            searchText = "~";
        }
        this.setState({searching: true});
        this.poiInfoUtil.search(searchText).then((items) => {
            this.setState({
                searching: false,
                items: items
            });
        });
    }

    getSearchResult() {
        const {items, helperText, searching} = this.state;
        const {onDetailsViewOpen} = this.props;
        if (searching) {
            return (<CircularProgress style={style.spinner} size={30}/>);
        } else {
            return (
                <GridList cellHeight={180} style={style.gridList}>
                    <Subheader>{helperText}</Subheader>
                    {items.map((tile) => (<GridTile
                                key={tile.id}
                                title={tile.name}
                                actionPosition="left"
                                titlePosition="top"
                                cols={2}
                                onClick={() => {onDetailsViewOpen(tile)}}
                                titleBackground="linear-gradient(to bottom, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
                                actionIcon={(
                                    <IconButton>
                                        <PlaceIcon color="white"/>
                                    </IconButton>
                                )}>
                                <img src={tile.originalUrlKey}/>
                            </GridTile>
                        ))}
                </GridList>
            )
        }
    }

    render() {
        return (
            <div style={style.container}>
                <SearchBar
                    onTextChange={this
                    .handleSearchTextChange
                    .bind(this)}/> {this.getSearchResult()}
            </div>
        )
    }
}