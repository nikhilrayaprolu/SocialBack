import React from 'react';
import FollowButton from "../followbutton";
import {handlefollow} from "../../utils";


class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: [],
            non_friend_items: [],
            userid: null,
        };
    }
    componentDidMount() {
        fetch("/api/friends")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result.friends,
                        non_friend_items: result.non_friends,
                        userid: result.userid
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    })
                }
            )
    }
    handlefollow(id) {
        handlefollow(this.state.userid, id, 'user');
    }
    displayitem(item, follow) {
        return (
            <div className="col-md-12 border-bottom" key={item.pk}>
                <div className="row">
                    <div className="col-md-2">
                        <img src="https://www.infrascan.net/demo/assets/img/avatar5.png"
                             className="img-circle" width="60px" />
                    </div>
                    <div className="col-md-6">
                        <h4><a href="#">{item.name} </a></h4>
                        <p><a href="#">School: {item.school}</a></p>
                        <p><a href="#">Class: {item.classname}</a></p>
                        <p><a href="#">Section: {item.section}</a></p>
                    </div>
                    <div className="col-md-2">
                        <FollowButton followed={follow} clicked={() => this.handlefollow(item.username)}/>
                    </div>
                </div>

            </div>
        )
    }
    render () {
        const { error, isLoaded, items, non_friend_items } = this.state;
        if (error) {
            return <React.Fragment><div>Error: {error.message}</div></React.Fragment>;
        } else if (!isLoaded) {
            return <React.Fragment><div>Loading...</div></React.Fragment>;
        } else {
            return (
                    <div className="container" id="react-feed">
                        <div className="shadow">
                            <div className="row">
                                {
                                    items.map(item => this.displayitem(item, true))
                                }
                                {
                                    non_friend_items.map(item => this.displayitem(item, false))
                                }
                            </div>
                        </div>
                    </div>
            );
        }
    }
}
export default Friends
