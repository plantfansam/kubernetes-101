import React from 'react'

export default class Service extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/concepts/services-networking/service/">Kubernetes Service</a></h3>
      </div>
    )
  }
}
