import React from 'react'

export default class ConfigMap extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.12/#configmap-v1-core">ConfigMap</a></h3>
      </div>
    )
  }
}
