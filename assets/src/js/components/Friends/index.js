import React from 'react';
import FollowButton from "../followbutton";


class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: [],
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
    getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    handlefollow(id) {
        var csrftoken = this.getCookie('csrftoken');
        var params =  {
            from_page: this.state.userid,
            to_page: id,
            type_of_page: 'user'
        };
        fetch("/api/follow/",{
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': csrftoken
    },
            method:"post",
            body: JSON.stringify(params),

        })
            .then(res => res.json())
            .then((result) => {
                console.log(result)
            },
                (error) => {
                console.log(error)
                })
    }

    render () {
        console.log("came into friends list");
        const { error, isLoaded, items } = this.state;
        if (error) {
            return <React.Fragment><div>Error: {error.message}</div></React.Fragment>;
        } else if (!isLoaded) {
            return <React.Fragment><div>Loading...</div></React.Fragment>;
        } else {
          return (
            <React.Fragment>
                <div className="container">
                    <div className="shadow">
                    <div className="row">
                    {items.map(item => (
                        <React.Fragment>
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
                                            <FollowButton clicked={() => this.handlefollow(item.username)}/>
                                            </div>
                                        </div>

                                    </div>
                        </React.Fragment>



                    ))}
                          </div>
                            </div>
                        </div>
            </React.Fragment>
          );
        }
      }
}
export default Friends
