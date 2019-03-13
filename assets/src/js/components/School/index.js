import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
class SchoolFeed extends React.Component {
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
        fetch("/api/moderator/"+this.props.match.params.schoolid)
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
        url.search = new URLSearchParams(options)
        console.log(url)
        return fetch(url).then(result =>{
            console.log(result)
            return result.json()
        })
    }
    doupdaterequest(params) {
        console.log(params)
        params['actor'] = params.actor.id
        var url = new URL(window.location.origin+'/getfeed/'+'school'+'/'+ this.props.match.params.schoolid);
        console.log(url)
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
        console.log("came into feed");
        let statusform = null;
        if (this.state.ismoderator){
            statusform = <StatusUpdateForm
          feedGroup="school"
          userId = { this.props.match.params.schoolid }
          doRequest = { this.doupdaterequest}
        />

        }
    return (
        <React.Fragment>
            {statusform}
         <FlatFeed
          options={{reactions: { recent: true } }}
          feedGroup = "school"
          userId = { this.props.match.params.schoolid }
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
export default SchoolFeed
