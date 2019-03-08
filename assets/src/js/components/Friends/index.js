import React from 'react';
class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
    }
    componentDidMount() {
        fetch("/api/friends")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result
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
        console.log("came into friends list");
        const { error, isLoaded, items } = this.state;
        if (error) {
            return <React.Fragment><div>Error: {error.message}</div></React.Fragment>;
        } else if (!isLoaded) {
            return <React.Fragment><div>Loading...</div></React.Fragment>;
        } else {
          return (
            <React.Fragment>
                <ul>
                    {items.map(item => (
                        <li key={item.user}>
                            {item.name} from {item.school} in class {item.class} {item.section}
                        </li>
                    ))}
                </ul>
            </React.Fragment>
          );
        }
      }
}
export default Friends
