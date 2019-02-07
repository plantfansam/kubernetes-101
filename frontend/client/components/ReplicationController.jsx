import React from 'react'

export default class ReplicationController extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/">Replication Controller</a></h3>
      </div>
    )
  }
}
