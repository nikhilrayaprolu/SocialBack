import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
class Footer extends React.Component {
    constructor(props) {
        super(props);
        console.log("inside footer", this.props)
        this.state = {
            approve: null,
            decline: null
        };
    }
    changefooter(approve, decline) {
        if(approve) {
            this.setState({
                approve: true,
                decline: null,
            })
        } else {
            this.setState({
                approve: null,
                decline: true,
            })
        }

    }
    render() {
        if(this.state.approve) {
            return (
                null
            )

        } else if (this.state.decline) {
            return (
                null
            )

        } else {
            return (
                <React.Fragment>
                    <Activity {...this.props}
                              Footer={() => (
                                  <div style={{padding: '8px 16px'}}>
                                      <button type="button" className="btn btn-primary" onClick={() => {this.props.activityapprove(this.props.activity.id, true, false);this.changefooter(true, null)}}>Approve</button>
                                      <button type="button" className="btn btn-danger" onClick={() => {this.props.activityapprove(this.props.activity.id, false, true);this.changefooter(null, true)}}>Decline</button>
                                  </div>
                              )}
                    />
                </React.Fragment>
            )

        }

    }

}
const UnMountActivityContext = React.createContext(null);
class UnApprovedGroup extends React.Component {
    constructor(props) {
        super(props);
        console.log("inside unapproved", this.props)
        this.state = {
            unmountedactivities: null,
        };
        this.activityapprove = this.activityapprove.bind(this);

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
    feedrequest(client, feedGroup, userId, options) {
        var url = new URL(window.location.origin+'/getfeed/'+feedGroup+'/'+userId);
        delete options['reactions'];
        url.search = new URLSearchParams(options)
        console.log(url)
        return fetch(url).then(result =>{
            console.log(result)
            return result.json()
        })
    }
    activityapprove(id, approve, decline){
        var csrftoken = this.getCookie('csrftoken');
        let params = {
            feed_id: id,
            feed_group: this.props.groupid,
            approve: approve,
            decline: decline
        };
        fetch("/api/approve/",{
            headers: {
                "Content-Type": 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken
    },
            method: 'post',
            body: JSON.stringify(params),
        })
            .then(res => res.json())
            .then(
                (result) => {
                    console.log('approved successfully')
                },
                (error) => {
                    console.log('approve unsuccessful')
                }
            )
    }
    render () {
        console.log("came into feed");
        let presentvalue = this.state.unmountedactivities;
        console.log(presentvalue);
        return (
            <React.Fragment>
                <FlatFeed
                    feedGroup = "unapprovedgroup"
                    userId = { this.props.groupid }
                    doFeedRequest = {this.feedrequest}
                    Activity={(props) => {
                        console.log(props, presentvalue);
                        //console.log(this.state.unmountedactivities.indexOf(props.activity.id));
                        return <Footer {...props} presentvalue={presentvalue} activityapprove={this.activityapprove} />
                    }
                    }


                />

            </React.Fragment>

        )
    }
}
export default UnApprovedGroup
