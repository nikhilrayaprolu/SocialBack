import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import {doupdaterequest, feedrequest, getCookie} from "../../utils";
class SchoolFeed extends React.Component {
    constructor(props) {
        super(props);
        this.doupdaterequest = this.doupdaterequest.bind(this);
        this.state = {
            error: null,
            isLoaded: false,
            ismoderator: false,
        };
        this.feedid = this.props.match.params.schoolid;
        this.feedgroup = "school"
    }
    componentDidMount() {
        var csrftoken = getCookie('csrftoken');
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
    doupdaterequest(params) {
            doupdaterequest(params, this.feedgroup, this.feedid)
    }

    render () {
        console.log("came into feed");
        let statusform = null;
        if (this.state.ismoderator){
            statusform = <StatusUpdateForm
          feedGroup={this.feedgroup}
          userId = { this.feedid }
          doRequest = { this.doupdaterequest}
        />

        }
    return (
        <React.Fragment>
            {statusform}
         <FlatFeed
          options={{reactions: { recent: true } }}
          feedGroup = {this.feedgroup}
          userId = { this.feedid }
          doFeedRequest = {feedrequest}
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
