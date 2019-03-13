import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import UnApprovedGroup from "../UnApprovedGroup";
class Group extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props)
        this.doupdaterequest = this.doupdaterequest.bind(this)
        this.state = {
            error: null,
            isLoaded: false,
            ismoderator: false,
        };

    }
    componentDidMount() {
        console.log('calling the api');
        var csrftoken = this.getCookie('csrftoken');
        fetch("/api/moderator/"+this.props.match.params.groupid)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        ismoderator: result.ismoderator
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
    feedrequest(client, feedGroup, userId, options) {
        var url = new URL(window.location.origin+'/getfeed/'+feedGroup+'/'+userId);
        delete options['reactions'];
        url.search = new URLSearchParams(options);
        console.log(url);
        return fetch(url).then(result =>{
            console.log(result);
            return result.json()
        })
    }
    doupdaterequest(params) {
        params['actor'] = params.actor.id;
        let url;
        if(this.state.ismoderator){
            url = new URL(window.location.origin+'/getfeed/'+'group'+'/'+ this.props.match.params.groupid);
        } else {
            url = new URL(window.location.origin+'/getfeed/'+'unapprovedgroup'+'/'+ this.props.match.params.groupid);
        }

        var csrftoken = this.getCookie('csrftoken');

        return fetch(url, {
            credentials: 'include',
            headers: {
                contentType: 'application/json; charset=utf-8',
        'X-CSRFToken': csrftoken
    },
            method:"post",
            body: JSON.stringify(params),

        }).then(result =>{
            console.log(result)
            return result.json()
        })
    }

    render () {
        console.log("came into group feeed");
        let unapprovedposts = null;
        if(this.state.ismoderator){
            unapprovedposts = <UnApprovedGroup groupid={this.props.match.params.groupid} />
        }
    return (
        <React.Fragment>
            <ul className="nav nav-pills">
                <li className="nav-item">
                    <a className="nav-link active" href="#">Global Group</a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" href="#">School Group</a>
                </li>
            </ul>
        <StatusUpdateForm
          feedGroup="globalgroup"
          userId = { this.props.match.params.groupid }
          doRequest = { this.doupdaterequest}
        />
            {unapprovedposts}
         <FlatFeed
          options={{reactions: { recent: true } }}
          feedGroup = "globalgroup"
          userId = { this.props.match.params.groupid }
          doFeedRequest = {this.feedrequest}
          Activity={(props) =>
              <Activity {...props}
                Footer={() => (
                  <div style={ {padding: '8px 16px'} }>
                    <LikeButton {...props} />
                    <CommentField
                      activity={props.activity}
                      onAddReaction={props.onAddReaction} />
                    <CommentList activityId={props.activity.id} />
                  </div>
                )}
              />
            }
          />

            </React.Fragment>

    )
  }
}
export default Group
