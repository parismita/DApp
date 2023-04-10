// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
  mapping(uint256 => User) users;
  mapping(uint256 => mapping(uint256 => uint256)) joint_acc_contribution;
  uint256 COUNT;
  uint256[] userlist; // store the userlist
  uint256[][] adj; // store the edgelist

  struct User {
    uint256 user_id;
    string user_name;
  }

  constructor () public {
    COUNT = 0;
  }

  function hasEdge(uint256 user_id_1, uint256 user_id_2) public returns (bool) {
    for (uint256 i = 0; i < adj[user_id_1].length; i++)
      if (adj[user_id_1][i] == user_id_2) 
        return true;
    return false;
  }

  function registerUser(uint256 user_id, string memory user_name) public {
    users[user_id] = User(user_id, user_name);
    userlist[COUNT] = user_id;
    COUNT++;
  }

  function createAcc(uint256 user_id_1, uint256 user_id_2, uint256 balance) public {
    require(!hasEdge(user_id_1, user_id_2));
    adj[user_id_1].push(user_id_2);
    adj[user_id_2].push(user_id_1);
    joint_acc_contribution[user_id_1][user_id_2] = balance/2;
    joint_acc_contribution[user_id_2][user_id_1] = balance/2;
  }

  function sendAmount(uint256 user_id_1, uint256 user_id_2) public {
    uint256[] memory path = shortestPath(user_id_1, user_id_2);
    bool satisfied = true;
    for (uint256 i = path.length - 1; i > 0; i--) {
      uint256 curr = path[i];
      uint256 next = path[i-1];
      if (joint_acc_contribution[curr][next] < 1) {
        satisfied = false;
        break;
      }
    }

    if (satisfied) {
      for (uint256 i = path.length - 1; i > 0; i--) {
        uint256 curr = path[i];
        uint256 next = path[i-1];
        joint_acc_contribution[curr][next] -= 1;
        joint_acc_contribution[next][curr] += 1;
      }
    }
  }

  function shortestPath(uint user_id_1, uint user_id_2) public returns (uint256[] memory) {
    uint256[] memory queue = new uint256[](COUNT+1);
    bool[] memory visited = new bool[](COUNT+1);
    uint256[] memory prev = new uint256[](COUNT+1);

    bool found = false;
    uint start = 0;
    uint end = 1;
    queue[start] = user_id_1;
    visited[user_id_1] = true;
    while(start < end)
    {
      uint256 curr = queue[start];
      start += 1;
      for (uint256 i = 0; i < adj[curr].length; i++)
      {
        uint256 next = adj[curr][i];
        if (!visited[next])
        {
          prev[next] = curr;
          visited[next] = true;
          queue[end] = next;
          end += 1;

          if (next == user_id_2)
            found = true;
            break;
        }
      }
      if (found)
        break;  
    }
    if (!found)
      return new uint256[](0);

    uint256[] memory path;
    uint256 j = 0;
    uint256 c = user_id_2;
    while(c != user_id_1)
    {
      path[j] = c;
      c = prev[c];
      j += 1;
    }
    path[j] = user_id_1;
    return path;
  }

  function closeAccount(uint256 user_id_1, uint256 user_id_2) public {
    require(hasEdge(user_id_1, user_id_2));
    for (uint256 i = 0; i < adj[user_id_1].length; i++)
      if (adj[user_id_1][i] == user_id_2) {
        adj[user_id_1][i] = adj[user_id_1][adj[user_id_1].length - 1];
        adj[user_id_1].pop();
        break;
      }
    for (uint256 i = 0; i < adj[user_id_2].length; i++)
      if (adj[user_id_2][i] == user_id_1) {
        adj[user_id_2][i] = adj[user_id_2][adj[user_id_2].length - 1];
        adj[user_id_2].pop();
        break;
      }
    delete joint_acc_contribution[user_id_1][user_id_2];
    delete joint_acc_contribution[user_id_2][user_id_1];
  }
}
