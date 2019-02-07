import React from 'react';

export default class Secret extends React.Component {
  render() {
    return (
      <div className={this.props.displayClass}>
        <h3><a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.12/#secret-v1-core">Secret</a></h3>
      </div>
    )
  }
}
