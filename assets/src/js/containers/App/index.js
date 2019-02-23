import React from 'react';
import Title from '../../components/Title';
import { StreamApp, NotificationDropdown, FlatFeed, LikeButton, Activity, CommentList, CommentField, StatusUpdateForm} from 'react-activity-feed';
import 'react-activity-feed/dist/index.css';


class App extends React.Component {
  render () {
    const text = 'Django + React + Webpack + Babel = Awesome App';
    return (
      <StreamApp
        apiKey="jkmk5yczhm7d"
        appId="48329"
        token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidXNlci1vbmUifQ.OT6TSv8GXRm-O7Qx7sFQZ-ScxJxEfzLzJc6znN6ufYY"
      >
        <NotificationDropdown notify/>
        <StatusUpdateForm
          feedGroup="timeline"
          userId="user-one" />
         <FlatFeed
          options={{reactions: { recent: true } }}
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
      </StreamApp>

    )
  }
}
export default App;
