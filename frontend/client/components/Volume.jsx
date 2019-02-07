import React from 'react';

export default class Volume extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/concepts/storage/volumes/">Volume</a></h3>
      </div>
    )
  }
}
