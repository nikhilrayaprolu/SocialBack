import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import {browserHistory} from 'react-router';
import {withRouter} from "react-router-dom";
import UserBar from "../YSUserBar";
class Home extends React.Component {

    render () {
        return (
            <React.Fragment>
                <div id="react-feed">
                <StatusUpdateForm
                    feedGroup="user"
                />
                <FlatFeed
                    options={{reactions: { recent: true } }}
                    notify
                    feedGroup="user"
                    Activity={(props) => {
                        return (
                            <Activity {...props}
                                      onClickUser = {(user) => {console.log(user);this.props.history.push(user.id)}}
                                      Header={() => (
                                          <UserBar {...props} />
                                      )}
                                      Header={() => (
                                          <UserBar {...props} />
                                      )}
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
                        )
                    }
                    }
                />
                </div>
            </React.Fragment>

        )
    }
}
export default withRouter(Home)
