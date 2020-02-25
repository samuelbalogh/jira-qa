import React from 'react'

const issues = ({ issues }) => {
  return (
    <div>
      <center><h1>Issues</h1></center>
        {issues.map((issue) => (
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{issue}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{issue}</h6>
              <p class="card-text">{issue}</p>
            </div>
          </div>
        ))}
      </div>
  )
}

export default issues
