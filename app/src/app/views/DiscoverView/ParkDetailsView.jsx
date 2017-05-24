import React, {Component} from 'react';

import {GridList, GridTile} from 'material-ui/GridList';
import IconButton from 'material-ui/IconButton';
import Paper from 'material-ui/Paper';
import Subheader from 'material-ui/Subheader';
import {List, ListItem} from 'material-ui/List';
import Chip from 'material-ui/Chip';

import {grey100} from 'material-ui/styles/colors';

import CloseIcon from 'material-ui/svg-icons/navigation/close';
import PlaceIcon from 'material-ui/svg-icons/maps/place';
import TypeIcon from 'material-ui/svg-icons/action/account-balance';
import PriceIcon from 'material-ui/svg-icons/editor/attach-money';
import LoyaltyIcon from 'material-ui/svg-icons/action/loyalty';
import PeopleIcon from 'material-ui/svg-icons/social/group';
import SmileIcon from 'material-ui/svg-icons/social/mood';

import POIReviewsUtil from '../../utils/POIReviewsUtil.jsx';

const style = {
    container: {
        background: grey100
    },
    headerPaper: {
        marginBottom: '20px',
        zIndex: 1
    },
    paper: {
        marginBottom: '20px',
        zIndex: 1
    },
    gridTile: {
        height: '240px',
        zIndex: 0
    },
    tileTitleStyle: {
        paddingTop: '20px',
        fontSize: '18px'
    },
    chip: {
        margin: '0px 4px 4px 0'
    },
    keywordContainer: {
        display: 'flex',
        flexWrap: 'wrap'
    }
}
export default class ParkDetailsView extends Component {
    constructor(state, props) {
        super(state, props);
        this.state = {
            reviews: null
        };

        this.poiReviewsUtil = new POIReviewsUtil();
    }

    componentWillMount() {
        this.getReviewsInfo(this.props.info.id);
    }

    getReviewsInfo(id) {
        this.poiReviewsUtil
            .get(id)
            .then((reviews) => {
                this.setState({reviews: reviews});
            });
    }

    getHeaderPaper() {
        const {onDetailsViewClose, info} = this.props;
        return (
            <Paper zDepth={1} style={style.headerPaper}>
                <GridTile
                    title={info.name}
                    actionPosition="left"
                    titlePosition="top"
                    cols={2}
                    style={style.gridTile}
                    titleStyle={style.tileTitleStyle}
                    titleBackground="linear-gradient(to bottom, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
                    actionIcon={(
                    <div style={style.tileTitleStyle}>
                        <IconButton
                            onTouchTap={onDetailsViewClose}>
                            <CloseIcon color="white"/>
                        </IconButton>
                    </div>
                )}>
                    <img src={info.originalUrlKey}/>
                </GridTile>
            </Paper>
        );
    }

    getBasicInfoPaper() {
        const {info} = this.props;
        return (
            <Paper zDepth={1} style={style.paper}>
                <List>
                    <Subheader>基本信息</Subheader>
                    <ListItem primaryText={info.regionName} leftIcon={< PlaceIcon />}/>
                    <ListItem primaryText={info.categoryName} leftIcon={< TypeIcon />}/>
                    <ListItem primaryText={info.priceText} leftIcon={< PriceIcon />}/>
                </List>
            </Paper>
        );
    }

    getExtractedInfoPaper() {
        const {reviews} = this.state;
        if (!reviews) 
            return null;
        
        return (
            <Paper zDepth={1} style={style.paper}>
                <List>
                    <Subheader>提取信息</Subheader>

                    <ListItem
                        secondaryText='关键词: 根据用户评论词频计算'
                        primaryText={(
                            <div style={style.keywordContainer}>
                                {reviews.keywords.map((keyword) => (
                                    <Chip key={keyword} style={style.chip}>
                                        {keyword}
                                    </Chip>
                                ))}
                            </div>)
                        }
                        leftIcon={< LoyaltyIcon />}/>
                    <ListItem
                        secondaryText='人群偏向/服务偏向: 根据用户评论时间计算'
                        primaryText={reviews.preferenceText}
                        leftIcon={< PeopleIcon />}/>
                    <ListItem
                        secondaryText='用户评价: 根据评论情感分析计算'
                        primaryText={reviews.sentimentsText}
                        leftIcon={< SmileIcon />}/>
                </List>
            </Paper>
        );
    }

    render() {
        return (
            <div style={style.container}>
                {this.getHeaderPaper()}
                {this.getExtractedInfoPaper()}
                {this.getBasicInfoPaper()}
            </div>
        );
    }
}