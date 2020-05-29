import React from 'react';
class GroupSideBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            schoolmates: 0,
            myfollowers 0,
            myfriends: 0,
        };
    }
    componentWillMount() {
        var csrftoken = getCookie('csrftoken');
        fetch("/youngwall/moderator/"+this.props.match.params.groupid)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        schoolmates: result.schoolmates,
                        myfollowers: result.myfollowers,
                        myfriends: result.myfriends
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

    render () {
        return (
            <React.Fragment>
               <p>Hello</p>
            </React.Fragment>
        )
    }
}
export default GroupSideBar
