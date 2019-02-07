import React from 'react';

export default class Ingress extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/concepts/workloads/pods/pod/">Pod</a></h3>
      </div>
    )
  }
}
