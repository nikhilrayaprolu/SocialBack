import React from 'react';
import { humanizeTimestamp } from '../../utils';
import { Dropdown, Link } from 'react-activity-feed';

/**
 * Component is described here.
 *
 * @example ./examples/UserBar.md
 */
export default class UserBar extends React.Component {
  render() {
      let timestamp = this.props.activity.time;
      let username = (this.props.activity.actor.data)? this.props.activity.actor.data.name: this.props.activity.actor;
        let time = humanizeTimestamp(timestamp);
        console.log(username);
    return (
      <div className="raf-user-bar">
        <div className="raf-user-bar__details">
            <div id="profileImage">{username[0]}</div>
          <p
            className="raf-user-bar__username"
            onClick={this.props.onClickUser}
          >
              {username}
          </p>
          {this.props.icon !== undefined ? (
            <img src={this.props.icon} alt="icon" />
          ) : null}
          {this.props.subtitle ? (
            <p className="raf-user-bar__subtitle">
              <time
                dateTime={time}
                title={time}
              >
                {this.props.subtitle}
              </time>
            </p>
          ) : null}
        </div>
        <React.Fragment>
            <span className="raf-user-bar__extra">
              <time
                dateTime={time}
                title={time}
              >
                {time}
              </time>
                <Dropdown>
                    <ul>
                        <li><Link onClick={() => {this.props.onRemoveActivity(this.props.activity.id);}}>Remove</Link></li>
                    </ul>
                </Dropdown>
            </span>
        </React.Fragment>
      </div>
    );
  }
}
