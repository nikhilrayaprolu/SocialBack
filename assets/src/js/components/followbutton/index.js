import React from 'react';

/**
 * Component is described here.
 *
 * @example ./examples/FollowButton.md
 */
export default class FollowButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { followed: this.props.followed || false };
  }

  render() {
    const { clicked, followed } = this.props;
    return (
      <div
        className={`raf-follow-button ${
          followed ? 'raf-follow-button--active' : ''
        }`}
        role="button"
        onClick={clicked}
      >
        {followed ? 'Following' : 'Follow'}
      </div>
    );
  }
}
