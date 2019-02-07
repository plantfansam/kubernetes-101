import React from 'react';

export default class Ingress extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/concepts/services-networking/ingress/">Ingress</a></h3>
      </div>
    )
  }
}
