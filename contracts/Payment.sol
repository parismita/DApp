// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract DynamicMapping {
    mapping(uint256 => uint256) public map;

    function update(uint256 key, uint256 val) public {
        map[key] = val;
    }

    function get(uint256 key) public view returns (uint256) {
        return map[key];
    }
}


contract Payment {
  mapping(uint256 => User) users;
  mapping(uint256 => uint256[]) adj; 
  mapping(uint256 => mapping(uint256 => uint256)) joint_acc_contribution;

  uint256 COUNT = 0;
  uint256[] userlist; // store the userlist

  struct User {
    uint256 user_id;
    string user_name;
    bool isRegistered;
  }

  event UserRegistered(uint256 user_id, string user_name);
  event AccountCreated(uint256 user_id_1, uint256 user_id_2, uint256 balance);

  function hasEdge(uint256 user_id_1, uint256 user_id_2) public view returns (bool) {
    for (uint256 i = 0; i < adj[user_id_1].length; i++)
      if (adj[user_id_1][i] == user_id_2) 
        return true;
    return false;
  }

  function registerUser(uint256 user_id, string memory user_name) public {
    require(users[user_id].isRegistered == false);
    users[user_id] = User(user_id, user_name, true);
    userlist.push(user_id);
    COUNT++;
    emit UserRegistered(user_id, user_name);
  }

  function getUser(uint256 user_id) public view returns (uint256, string memory, bool, uint256[] memory) {
    User memory user = users[user_id];
    return (user.user_id, user.user_name, user.isRegistered, adj[user_id]);
  }

  function getAllUsers() public view returns (uint256[] memory) {
    return userlist;
  }

  function createAcc(uint256 user_id_1, uint256 user_id_2, uint256 balance) public {
    require(!hasEdge(user_id_1, user_id_2));
    adj[user_id_1].push(user_id_2);
    adj[user_id_2].push(user_id_1);
    joint_acc_contribution[user_id_1][user_id_2] = balance/2;
    joint_acc_contribution[user_id_2][user_id_1] = balance/2;
    emit AccountCreated(user_id_1, user_id_2, balance);
  }

  function getAcc(uint256 user_id_1, uint256 user_id_2) public view returns (uint256, uint256, uint256, uint256) {
    require(hasEdge(user_id_1, user_id_2));
    return (user_id_1, user_id_2, joint_acc_contribution[user_id_1][user_id_2], joint_acc_contribution[user_id_2][user_id_1]);
  }

  function sendAmount(uint256 user_id_1, uint256 user_id_2) public {
    uint256[] memory path = shortestPath(user_id_1, user_id_2);
    require(path.length > 0);

    bool satisfied = true;
    for (uint256 i = 0; i < path.length - 1; i++) {
      uint256 curr = path[i];
      uint256 next = path[i+1];
      if (joint_acc_contribution[curr][next] < 1000) {
        satisfied = false;
        break;
      }
    }
    require(satisfied);

    if (satisfied) {
      for (uint256 i = 0; i < path.length - 1; i++) {
        uint256 curr = path[i];
        uint256 next = path[i+1];
        joint_acc_contribution[curr][next] -= 1000;
        joint_acc_contribution[next][curr] += 1000;
      }
    }
  }

  function getFailureReason(uint256 user_id_1, uint256 user_id_2) public returns (uint256[] memory, uint256[] memory) {
    uint256[] memory path = shortestPath(user_id_1, user_id_2);
    uint256[] memory balances = new uint256[](path.length-1);
    
    for (uint256 i = 0; i < path.length - 1; i++) {
      uint256 curr = path[i];
      uint256 next = path[i+1];
      balances[i] = joint_acc_contribution[curr][next];
    }

    return (path, balances);
  }


  function shortestPath(uint256 user_id_1, uint256 user_id_2) public returns (uint256[] memory) {
    uint256[] memory queue = new uint256[](COUNT+1);
    DynamicMapping visited = new DynamicMapping();
    DynamicMapping prev = new DynamicMapping();

    bool found = false;
    uint start = 0;
    uint end = 1;
    queue[start] = user_id_1;
    visited.update(user_id_1, 1);
    while(start < end)
    {
      uint256 curr = queue[start];
      start += 1;
      for (uint256 i = 0; i < adj[curr].length; i++)
      {
        uint256 next = adj[curr][i];
        if (visited.get(next) == 0)
        {
          visited.update(next, 1);
          if (joint_acc_contribution[curr][next] < 1000)
            continue;
          prev.update(next, curr);
          queue[end] = next;
          end++;

          if (next == user_id_2) {
            found = true;
            break;
          }
        }
      }
      if (found)
        break;  
    }
    if (!found)
      return new uint256[](0);

    uint depth = 1;
    uint256 c = user_id_2;
    while(c != user_id_1) {
      depth++;
      c = prev.get(c);
    }

    uint256[] memory path = new uint256[](depth);
    c = user_id_2;
    for (uint256 i = 0; i < depth; i++) {
      path[depth - i - 1] = c;
      c = prev.get(c);
    }
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
