import React from 'react';
import FollowButton from "../followbutton";
import {handlefollow} from "../../utils";


export default class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: [],
            non_friend_items: [],
            userid: null,
            school: "",
            classLevel: "",
            section: "",
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChangeschool = this.handleChangeschool.bind(this);
        this.handleChangeclass = this.handleChangeclass.bind(this);
        this.handleChangesection = this.handleChangesection.bind(this);
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
    handleSubmit(event) {
        event.preventDefault();
        let q = "/api/search/user?";
        if(this.state.school)
            q += "school=" + this.state.school + "&";
        if(this.state.classLevel)
            q += "class=" + this.state.classLevel + "&";
        if(this.state.section)
            q += "section=" + this.state.section;
        fetch(q)
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
    handleChangeschool(event) {
        this.setState({school: event.target.value});
    }
    handleChangeclass(event) {
        this.setState({classLevel: event.target.value});
    }
    handleChangesection(event) {
        this.setState({section: event.target.value});
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
                        <p><a href="#">School: {item.schoolname}</a></p>
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
            return <React.Fragment><div className="container" id="react-feed"><h2>Loading...</h2></div></React.Fragment>;
        } else {
            return (
                    <div className="container" id="react-feed">
                        <div className="searchbar">
                            <form onSubmit={this.handleSubmit}>
                                <div className="form-group">
                                    <input type="text" className="form-control" placeholder="Enter School" value={this.state.school} onChange={this.handleChangeschool} />
                                </div>
                                <div className="select-container">
                                    <div className="form-group">
                                        <label htmlFor="class">Class:</label>
                                        <select className="form-control" value={this.state.classLevel} onChange={this.handleChangeclass}>
                                            <option value="">All</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                        </select>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="section">Section:</label>
                                        <select className="form-control" value={this.state.section} onChange={this.handleChangesection}>
                                            <option value="">All</option>
                                            <option value="A">A</option>
                                            <option value="B">B</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="button-container">
                                    <button type="submit" value="Submit" className="btn btn-primary">Search</button>
                                </div>
                            </form>
                        </div>
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
