import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
class Group extends React.Component {
    feedrequest (...arr) {
        console.log(arr)
    }
    render () {
        console.log("came into feed");
    return (
        <React.Fragment>
         <FlatFeed
          options={{reactions: { recent: true } }}
          feedGroup = "globalgroup"
          userId = { this.props.match.params.groupid }
          doFeedRequest = {this.feedrequest}
          notify
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
